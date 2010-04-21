"""
:mod:`DBAdapters` -- database adapters for statistics
=====================================================================

.. warning:: the use the of a DB Adapter can reduce the performance of the
             Genetic Algorithm.

Pyevolve have a feature in which you can save the statistics of every
generation in a database, file or call an URL with the statistics as param.
You can use the database to plot evolution statistics graphs later. In this
module, you'll find the adapters above cited.

.. seealso::

   Method :meth:`GSimpleGA.GSimpleGA.setDBAdapter`
      DB Adapters are set in the GSimpleGA Class.

"""

from pyevolve import __version__
import Consts
import Util
import logging
import types
import datetime
import Statistics


class DBBaseAdapter:
   """ DBBaseAdapter Class - The base class for all DB Adapters

   If you want to create your own DB Adapter, you must subclass this
   class.

   :param frequency: the the generational dump frequency

   .. versionadded:: 0.6
      Added the :class:`DBBaseAdapter` class.
   """
   def __init__(self, frequency, identify):
      """ The class constructor """
      self.statsGenFreq = frequency

      if identify is None:
         self.identify = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%y-%H:%M")
      else:
         self.identify = identify

   def setIdentify(self, identify):
      """ Sets the identify of the statistics
      
      :param identify: the id string
      """
      if identify is None:
         self.identify = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%y-%H:%M")
      else:
         self.identify = identify

   def getIdentify(self):
      """ Return the statistics identify
      
      :rtype: identify string
      """
      return self.identify

   def getStatsGenFreq(self):
      """ Returns the frequency of statistical dump
      
      :rtype: the generation interval of statistical dump
      """
      return self.statsGenFreq

   def setStatsGenFreq(self, statsGenFreq):
      """ Set the frequency of statistical dump
      
      :param statsGenFreq: the generation interval of statistical dump
      """
      self.statsGenFreq = statsGenFreq

   def open(self, ga_engine):
      """ This method is called one time to do the initialization of
      the DB Adapter

      :param ga_engine: the GA Engine
      """
      pass

   def commitAndClose(self):
      """ This method is called at the end of the evolution, to closes the
      DB Adapter and commit the changes """
      pass

   def insert(self, ga_engine):
      """ Insert the stats

      :param ga_engine: the GA Engine
      """
      Util.raiseException("This method is not implemented on the ABC", NotImplementedError)

class DBFileCSV(DBBaseAdapter):
   """ DBFileCSV Class - Adapter to dump statistics in CSV format

   Inheritance diagram for :class:`DBAdapters.DBFileCSV`:

   .. inheritance-diagram:: DBAdapters.DBFileCSV

   Example:
      >>> adapter = DBFileCSV(filename="file.csv", identify="run_01",
                              frequency = 1, reset = True)

      :param filename: the CSV filename
      :param identify: the identify of the run
      :param frequency: the generational dump frequency
      :param reset: if is True, the file old data will be overwrite with the new

   .. versionadded:: 0.6
      Removed the stub methods and subclassed the :class:`DBBaseAdapter` class.

   """
   def __init__(self, filename=Consts.CDefCSVFileName, identify=None,
                frequency = Consts.CDefCSVFileStatsGenFreq, reset=True):
      """ The creator of DBFileCSV Class """

      DBBaseAdapter.__init__(self, frequency, identify)
      
      self.csvmod = None

      self.filename = filename
      self.csvWriter = None
      self.fHandle = None
      self.reset = reset

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBFileCSV DB Adapter [File='%s', identify='%s']" % (self.filename, self.getIdentify())
      return ret

   def open(self, ga_engine):
      """ Open the CSV file or creates a new file

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      if self.csvmod is None:
         logging.debug("Loading the csv module...")
         self.csvmod = Util.importSpecial("csv")

      logging.debug("Opening the CSV file to dump statistics [%s]", self.filename)
      if self.reset: open_mode = "w"
      else: open_mode = "a"
      self.fHandle = open(self.filename, open_mode)
      self.csvWriter = self.csvmod.writer(self.fHandle, delimiter=';')

   def close(self):
      """ Closes the CSV file handle """
      logging.debug("Closing the CSV file [%s]", self.filename)
      if self.fHandle:
         self.fHandle.close()

   def commitAndClose(self):
      """ Commits and closes """
      self.close()

   def insert(self, ga_engine):
      """ Inserts the stats into the CSV file

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      stats = ga_engine.getStatistics()
      generation = ga_engine.getCurrentGeneration()
      line = [self.getIdentify(), generation]
      line.extend(stats.asTuple())
      self.csvWriter.writerow(line)

class DBURLPost(DBBaseAdapter):
   """ DBURLPost Class - Adapter to call an URL with statistics

   Inheritance diagram for :class:`DBAdapters.DBURLPost`:

   .. inheritance-diagram:: DBAdapters.DBURLPost

   Example:
      >>> dbadapter = DBURLPost(url="http://localhost/post.py", identify="test")

   The parameters that will be sent is all the statistics described in the :class:`Statistics.Statistics`
   class, and the parameters:
   
   **generation**
      The generation of the statistics

   **identify**
      The id specified by user

   .. note:: see the :class:`Statistics.Statistics` documentation.

   :param url: the URL to be used
   :param identify: the identify of the run
   :param frequency: the generational dump frequency
   :param post: if True, the POST method will be used, otherwise GET will be used.

   .. versionadded:: 0.6
      Removed the stub methods and subclassed the :class:`DBBaseAdapter` class.
   """
   
   def __init__(self, url, identify=None,
                frequency = Consts.CDefURLPostStatsGenFreq, post=True):
      """ The creator of the DBURLPost Class. """

      DBBaseAdapter.__init__(self, frequency, identify)
      self.urllibmod = None

      self.url = url
      self.post = post

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBURLPost DB Adapter [URL='%s', identify='%s']" % (self.url, self.getIdentify())
      return ret

   def open(self, ga_engine):
      """ Load the modules needed

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      if self.urllibmod is None:
         logging.debug("Loading urllib module...")
         self.urllibmod = Util.importSpecial("urllib")

   def insert(self, ga_engine):
      """ Sends the data to the URL using POST or GET

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      logging.debug("Sending http request to %s.", self.url)
      stats = ga_engine.getStatistics()
      response = None
      params = stats.internalDict.copy()
      params["generation"] = ga_engine.getCurrentGeneration()
      params["identify"] = self.getIdentify()
      if self.post: # POST
         response = self.urllibmod.urlopen(self.url, self.urllibmod.urlencode(params))
      else: # GET
         response = self.urllibmod.urlopen(self.url + "?%s" % (self.urllibmod.urlencode(params)))
      if response: response.close()

class DBSQLite(DBBaseAdapter):
   """ DBSQLite Class - Adapter to dump data in SQLite3 database format
   
   Inheritance diagram for :class:`DBAdapters.DBSQLite`:

   .. inheritance-diagram:: DBAdapters.DBSQLite

   Example:
      >>> dbadapter = DBSQLite(identify="test")

   When you run some GA for the first time, you need to create the database, for this, you
   must use the *resetDB* parameter:

      >>> dbadapter = DBSQLite(identify="test", resetDB=True)

   This parameter will erase all the database tables and will create the new ones.
   The *resetDB* parameter is different from the *resetIdentify* parameter, the *resetIdentify*
   only erases the rows with the same "identify" name.   

   :param dbname: the database filename
   :param identify: the identify if the run
   :param resetDB: if True, the database structure will be recreated
   :param resetIdentify: if True, the identify with the same name will be overwrite with new data
   :param frequency: the generational dump frequency
   :param commit_freq: the commit frequency
   """

   def __init__(self, dbname=Consts.CDefSQLiteDBName, identify=None, resetDB=False,
                resetIdentify=True, frequency=Consts.CDefSQLiteStatsGenFreq,
                commit_freq=Consts.CDefSQLiteStatsCommitFreq):
      """ The creator of the DBSQLite Class """

      DBBaseAdapter.__init__(self, frequency, identify)

      self.sqlite3mod = None
      self.connection = None
      self.resetDB = resetDB
      self.resetIdentify = resetIdentify
      self.dbName = dbname
      self.typeDict = { types.FloatType : "real" }
      self.cursorPool = None
      self.commitFreq = commit_freq

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBSQLite DB Adapter [File='%s', identify='%s']" % (self.dbName, self.getIdentify())
      return ret

   def open(self, ga_engine):
      """ Open the database connection

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      if self.sqlite3mod is None:
         logging.debug("Loading sqlite3 module...")
         self.sqlite3mod = Util.importSpecial("sqlite3")

      logging.debug("Opening database, dbname=%s", self.dbName)
      self.connection = self.sqlite3mod.connect(self.dbName)

      temp_stats = Statistics.Statistics()

      if self.resetDB:
         self.resetStructure(Statistics.Statistics())

      self.createStructure(temp_stats)

      if self.resetIdentify:
         self.resetTableIdentify()

   def commitAndClose(self):
      """ Commit changes on database and closes connection """
      self.commit()
      self.close()

   def close(self):
      """ Close the database connection """
      logging.debug("Closing database.")
      if self.cursorPool:
         self.cursorPool.close()
         self.cursorPool = None
      self.connection.close()

   def commit(self):
      """ Commit changes to database """
      logging.debug("Commiting changes to database.")
      self.connection.commit()

   def getCursor(self):
      """ Return a cursor from the pool

      :rtype: the cursor

      """
      if not self.cursorPool:
         logging.debug("Creating new cursor for database...")
         self.cursorPool = self.connection.cursor()
         return self.cursorPool
      else:
         return self.cursorPool

   def createStructure(self, stats):
      """ Create table using the Statistics class structure

      :param stats: the statistics object

      """
      c = self.getCursor()
      pstmt = "create table if not exists %s(identify text, generation integer, " % (Consts.CDefSQLiteDBTable)
      for k, v in stats.items():
         pstmt += "%s %s, " % (k, self.typeDict[type(v)])
      pstmt = pstmt[:-2] + ")"
      logging.debug("Creating table %s: %s.", Consts.CDefSQLiteDBTable, pstmt)
      c.execute(pstmt)

      pstmt = """create table if not exists %s(identify text, generation integer,
              individual integer, fitness real, raw real)""" % (Consts.CDefSQLiteDBTablePop)
      logging.debug("Creating table %s: %s.", Consts.CDefSQLiteDBTablePop, pstmt)
      c.execute(pstmt)
      self.commit()

   def resetTableIdentify(self):
      """ Delete all records on the table with the same Identify """
      c = self.getCursor()
      stmt  = "delete from %s where identify = ?" % (Consts.CDefSQLiteDBTable)
      stmt2 = "delete from %s where identify = ?" % (Consts.CDefSQLiteDBTablePop)

      logging.debug("Erasing data from the tables with the identify = %s", self.getIdentify())
      try:
         c.execute(stmt, (self.getIdentify(),))
         c.execute(stmt2, (self.getIdentify(),))
      except self.sqlite3mod.OperationalError, expt:
         if str(expt).find("no such table") >= 0:
            print "\n ## The DB Adapter can't find the tables ! Consider enable the parameter resetDB ! ##\n"

      self.commit()


   def resetStructure(self, stats):
      """ Deletes de current structure and calls createStructure

      :param stats: the statistics object

      """
      logging.debug("Reseting structure, droping table and creating new empty table.")
      c = self.getCursor()
      c.execute("drop table if exists %s" % (Consts.CDefSQLiteDBTable,))
      c.execute("drop table if exists %s" % (Consts.CDefSQLiteDBTablePop,))
      self.commit()
      self.createStructure(stats)
      
   def insert(self, ga_engine):
      """ Inserts the statistics data to database

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      stats      = ga_engine.getStatistics()
      population = ga_engine.getPopulation()
      generation = ga_engine.getCurrentGeneration()

      c = self.getCursor()
      pstmt = "insert into %s values (?, ?, " % (Consts.CDefSQLiteDBTable)
      for i in xrange(len(stats)):
         pstmt += "?, "
      pstmt = pstmt[:-2] + ")" 
      c.execute(pstmt, (self.getIdentify(), generation) + stats.asTuple())

      pstmt = "insert into %s values(?, ?, ?, ?, ?)" % (Consts.CDefSQLiteDBTablePop,)
      tups = []
      for i in xrange(len(population)):
         ind = population[i]
         tups.append((self.getIdentify(), generation, i, ind.fitness, ind.score))

      c.executemany(pstmt, tups)
      if (generation % self.commitFreq == 0):
         self.commit()

class DBXMLRPC(DBBaseAdapter):
   """ DBXMLRPC Class - Adapter to dump statistics to a XML Remote Procedure Call

   Inheritance diagram for :class:`DBAdapters.DBXMLRPC`:

   .. inheritance-diagram:: DBAdapters.DBXMLRPC

   Example:
      >>> adapter = DBXMLRPC(url="http://localhost:8000/", identify="run_01",
                             frequency = 1)

      :param url: the URL of the XML RPC
      :param identify: the identify of the run
      :param frequency: the generational dump frequency


   .. note:: The XML RPC Server must implement the *insert* method, wich receives
             a python dictionary as argument.
   
   Example of an server in Python: ::

      import xmlrpclib
      from SimpleXMLRPCServer import SimpleXMLRPCServer

      def insert(l):
          print "Received statistics: %s" % l

      server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
      print "Listening on port 8000..."
      server.register_function(insert, "insert")
      server.serve_forever()

   .. versionadded:: 0.6
      The :class:`DBXMLRPC` class.

   """
   def __init__(self, url, identify=None, frequency = Consts.CDefXMLRPCStatsGenFreq):
      """ The creator of DBXMLRPC Class """

      DBBaseAdapter.__init__(self, frequency, identify)
      self.xmlrpclibmod = None

      self.url = url
      self.proxy = None

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBXMLRPC DB Adapter [URL='%s', identify='%s']" % (self.url, self.getIdentify())
      return ret

   def open(self, ga_engine):
      """ Open the XML RPC Server proxy

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      if self.xmlrpclibmod is None:
         logging.debug("Loding the xmlrpclib module...")
         self.xmlrpclibmod = Util.importSpecial("xmlrpclib")

      logging.debug("Opening the XML RPC Server Proxy on %s", self.url)
      self.proxy = self.xmlrpclibmod.ServerProxy(self.url, allow_none=True)

   def insert(self, ga_engine):
      """ Calls the XML RPC procedure

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      stats = ga_engine.getStatistics()
      generation = ga_engine.getCurrentGeneration()
      di = stats.internalDict.copy()
      di.update({"identify": self.getIdentify(), "generation": generation})
      self.proxy.insert(di)

class DBVPythonGraph(DBBaseAdapter):
   """ The DBVPythonGraph Class - A DB Adapter for real-time visualization using VPython

   Inheritance diagram for :class:`DBAdapters.DBVPythonGraph`:

   .. inheritance-diagram:: DBAdapters.DBVPythonGraph

   .. note:: to use this DB Adapter, you **must** install VPython first.

   Example:
      >>> adapter = DBAdapters.DBVPythonGraph(identify="run_01", frequency = 1)
      >>> ga_engine.setDBAdapter(adapter)
   
   :param identify: the identify of the run
   :param genmax: use the generations as max value for x-axis, default False
   :param frequency: the generational dump frequency

   .. versionadded:: 0.6
      The *DBVPythonGraph* class.
   """

   def __init__(self, identify=None, frequency = 20, genmax=False):
      DBBaseAdapter.__init__(self, frequency, identify)
      self.genmax = genmax
      self.vtkGraph = None
      self.curveMin = None
      self.curveMax = None
      self.curveDev = None
      self.curveAvg = None

   def makeDisplay(self, title_sec, x, y, ga_engine):
      """ Used internally to create a new display for VPython.
      
      :param title_sec: the title of the window
      :param x: the x position of the window
      :param y: the y position of the window
      :param ga_engine: the GA Engine

      :rtype: the window (the return of gdisplay call)
      """
      title = "Pyevolve v.%s - %s - id [%s]" % (__version__, title_sec, self.identify)
      if self.genmax:
         disp = self.vtkGraph.gdisplay(title=title, xtitle='Generation', ytitle=title_sec,
                                    xmax=ga_engine.getGenerations(), xmin=0., width=500,
                                    height=250, x=x, y=y)
      else:
         disp = self.vtkGraph.gdisplay(title=title, xtitle='Generation', ytitle=title_sec,
                                    xmin=0., width=500, height=250, x=x, y=y)
         return disp

   def open(self, ga_engine):
      """ Imports the VPython module and creates the four graph windows

      :param ga_engine: the GA Engine
      """
      logging.debug("Loading visual.graph (VPython) module...")
      if self.vtkGraph is None:
         self.vtkGraph = Util.importSpecial("visual.graph").graph

      display_rawmin = self.makeDisplay("Raw Score (min)",       0,   0,   ga_engine)
      display_rawmax = self.makeDisplay("Raw Score (max)",       0,   250, ga_engine)
      display_rawdev = self.makeDisplay("Raw Score (std. dev.)", 500, 0,   ga_engine)
      display_rawavg = self.makeDisplay("Raw Score (avg)",       500, 250, ga_engine)

      self.curveMin = self.vtkGraph.gcurve(color=self.vtkGraph.color.red,    gdisplay=display_rawmin)
      self.curveMax = self.vtkGraph.gcurve(color=self.vtkGraph.color.green,  gdisplay=display_rawmax)
      self.curveDev = self.vtkGraph.gcurve(color=self.vtkGraph.color.blue,   gdisplay=display_rawdev)
      self.curveAvg = self.vtkGraph.gcurve(color=self.vtkGraph.color.orange, gdisplay=display_rawavg)

   def insert(self, ga_engine):
      """ Plot the current statistics to the graphs

      :param ga_engine: the GA Engine
      """
      stats = ga_engine.getStatistics()
      generation = ga_engine.getCurrentGeneration()

      self.curveMin.plot(pos=(generation, stats["rawMin"]))
      self.curveMax.plot(pos=(generation, stats["rawMax"]))
      self.curveDev.plot(pos=(generation, stats["rawDev"]))
      self.curveAvg.plot(pos=(generation, stats["rawAve"]))
      
class DBMySQLAdapter(DBBaseAdapter):
   """ DBMySQLAdapter Class - Adapter to dump data in MySql database server

   Inheritance diagram for :class:`DBAdapters.DBMySQLAdapter`:

   .. inheritance-diagram:: DBAdapters.DBMySQLAdapter

   Example:
      >>> dbadapter = DBMySQLAdapter("pyevolve_username", "password", identify="run1")

   or

      >>> dbadapter = DBMySQLAdapter(user="username", passwd="password",
      ...                            host="mysqlserver.com.br", port=3306, db="pyevolve_db")

   When you run some GA for the first time, you need to create the database, for this, you
   must use the *resetDB* parameter as True.

   This parameter will erase all the database tables and will create the new ones.
   The *resetDB* parameter is different from the *resetIdentify* parameter, the *resetIdentify*
   only erases the rows with the same "identify" name, and *resetDB* will drop and recreate
   the tables.

   :param user: mysql username (must have permission to create, drop, insert, etc.. on tables
   :param passwd: the user password on MySQL server
   :param host: the hostname, default is "localhost"
   :param port: the port, default is 3306
   :param db: the database name, default is "pyevolve"
   :param identify: the identify if the run
   :param resetDB: if True, the database structure will be recreated
   :param resetIdentify: if True, the identify with the same name will be overwrite with new data
   :param frequency: the generational dump frequency
   :param commit_freq: the commit frequency
   """

   def __init__(self, user, passwd, host=Consts.CDefMySQLDBHost, port=Consts.CDefMySQLDBPort,
                db=Consts.CDefMySQLDBName, identify=None, resetDB=False, resetIdentify=True,
                frequency=Consts.CDefMySQLStatsGenFreq, commit_freq=Consts.CDefMySQLStatsCommitFreq):
      """ The creator of the DBSQLite Class """

      DBBaseAdapter.__init__(self, frequency, identify)

      self.mysqldbmod = None
      self.connection = None
      self.resetDB = resetDB
      self.resetIdentify = resetIdentify
      self.db = db
      self.host = host
      self.port = port
      self.user = user
      self.passwd = passwd
      self.typeDict = { types.FloatType : "DOUBLE(14,6)" }
      self.cursorPool = None
      self.commitFreq = commit_freq

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBMySQLAdapter DB Adapter [identify='%s', host='%s', username='%s', db='%s']" % (self.getIdentify(),
            self.host, self.user, self.db)
      return ret

   def open(self, ga_engine):
      """ Open the database connection

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      if self.mysqldbmod is None:
         logging.debug("Loading MySQLdb module...")
         self.mysqldbmod = Util.importSpecial("MySQLdb")

      logging.debug("Opening database, host=%s", self.host)
      self.connection = self.mysqldbmod.connect(host=self.host, user=self.user,
                                                passwd=self.passwd, db=self.db,
                                                port=self.port)
      temp_stats = Statistics.Statistics()
      self.createStructure(temp_stats)

      if self.resetDB:
         self.resetStructure(Statistics.Statistics())

      if self.resetIdentify:
         self.resetTableIdentify()

   def commitAndClose(self):
      """ Commit changes on database and closes connection """
      self.commit()
      self.close()

   def close(self):
      """ Close the database connection """
      logging.debug("Closing database.")
      if self.cursorPool:
         self.cursorPool.close()
         self.cursorPool = None
      self.connection.close()

   def commit(self):
      """ Commit changes to database """
      logging.debug("Commiting changes to database.")
      self.connection.commit()

   def getCursor(self):
      """ Return a cursor from the pool

      :rtype: the cursor

      """
      if not self.cursorPool:
         logging.debug("Creating new cursor for database...")
         self.cursorPool = self.connection.cursor()
         return self.cursorPool
      else:
         return self.cursorPool

   def createStructure(self, stats):
      """ Create table using the Statistics class structure

      :param stats: the statistics object

      """
      c = self.getCursor()
      pstmt = "create table if not exists %s(identify VARCHAR(80), generation INTEGER, " % (Consts.CDefMySQLDBTable)
      for k, v in stats.items():
         pstmt += "%s %s, " % (k, self.typeDict[type(v)])
      pstmt = pstmt[:-2] + ")"
      logging.debug("Creating table %s: %s.", Consts.CDefSQLiteDBTable, pstmt)
      c.execute(pstmt)

      pstmt = """create table if not exists %s(identify VARCHAR(80), generation INTEGER,
              individual INTEGER, fitness DOUBLE(14,6), raw DOUBLE(14,6))""" % (Consts.CDefMySQLDBTablePop)
      logging.debug("Creating table %s: %s.", Consts.CDefMySQLDBTablePop, pstmt)
      c.execute(pstmt)
      self.commit()

   def resetTableIdentify(self):
      """ Delete all records on the table with the same Identify """
      c = self.getCursor()
      stmt  = "delete from %s where identify = '%s'" % (Consts.CDefMySQLDBTable, self.getIdentify())
      stmt2 = "delete from %s where identify = '%s'" % (Consts.CDefMySQLDBTablePop, self.getIdentify())

      logging.debug("Erasing data from the tables with the identify = %s", self.getIdentify())
      c.execute(stmt)
      c.execute(stmt2)

      self.commit()


   def resetStructure(self, stats):
      """ Deletes de current structure and calls createStructure

      :param stats: the statistics object

      """
      logging.debug("Reseting structure, droping table and creating new empty table.")
      c = self.getCursor()
      c.execute("drop table if exists %s" % (Consts.CDefMySQLDBTable,))
      c.execute("drop table if exists %s" % (Consts.CDefMySQLDBTablePop,))
      self.commit()
      self.createStructure(stats)
      
   def insert(self, ga_engine):
      """ Inserts the statistics data to database

      :param ga_engine: the GA Engine

      .. versionchanged:: 0.6
         The method now receives the *ga_engine* parameter.
      """
      stats      = ga_engine.getStatistics()
      population = ga_engine.getPopulation()
      generation = ga_engine.getCurrentGeneration()

      c = self.getCursor()
      pstmt = "insert into " + Consts.CDefMySQLDBTable + " values (%s, %s, "
      for i in xrange(len(stats)):
         pstmt += "%s, "
      pstmt = pstmt[:-2] + ")" 
      c.execute(pstmt, (self.getIdentify(), generation) + stats.asTuple())

      pstmt = "insert into " + Consts.CDefMySQLDBTablePop + " values(%s, %s, %s, %s, %s)"

      tups = []
      for i in xrange(len(population)):
         ind = population[i]
         tups.append((self.getIdentify(), generation, i, ind.fitness, ind.score))

      c.executemany(pstmt, tups)
      if (generation % self.commitFreq == 0):
         self.commit()
