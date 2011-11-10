#!/usr/bin/python

# This code is part of Pyevolve.
# It requires matplotlib v.0.98.5.0+
from optparse import OptionParser
from optparse import OptionGroup

def graph_pop_heatmap_raw(pop, minimize, colormap="jet", filesave=None):
   pylab.imshow(pop, aspect="auto", interpolation="gaussian", cmap=matplotlib.cm.__dict__[colormap])
   pylab.title("Plot of pop. raw scores along the generations")
   pylab.xlabel('Population')
   pylab.ylabel('Generations')
   pylab.grid(True)
   pylab.colorbar()

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_pop_heatmap_fitness(pop, minimize, colormap="jet", filesave=None):
   pylab.imshow(pop, aspect="equal", interpolation="gaussian", cmap=matplotlib.cm.__dict__[colormap])
   pylab.title("Plot of pop. fitness scores along the generations")
   pylab.xlabel('Population')
   pylab.ylabel('Generations')
   pylab.grid(True)
   pylab.colorbar()

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()


def graph_diff_raw(pop, minimize, filesave=None):
   x = []

   diff_raw_y = []
   diff_fit_y = []

   for it in pop:
      x.append(it["generation"])
      diff_raw_y.append(it["rawMax"] - it["rawMin"])
      diff_fit_y.append(it["fitMax"] - it["fitMin"])

   pylab.figure()
   pylab.subplot(211)
   
   pylab.plot(x, diff_raw_y, "g", label="Raw difference", linewidth=1.2)
   pylab.fill_between(x, diff_raw_y, color="g", alpha=0.1)

   diff_raw_max= max(diff_raw_y)
   gen_max_raw = x[diff_raw_y.index(diff_raw_max)]

   pylab.annotate("Maximum (%.2f)" % (diff_raw_max,), xy=(gen_max_raw, diff_raw_max),  xycoords='data',
                xytext=(-150, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Raw difference")
   pylab.title("Plot of evolution identified by '%s'" % (options.identify))

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   pylab.subplot(212) 

   pylab.plot(x, diff_fit_y, "b", label="Fitness difference", linewidth=1.2)
   pylab.fill_between(x, diff_fit_y, color="b", alpha=0.1)


   diff_fit_max= max(diff_fit_y)
   gen_max_fit = x[diff_fit_y.index(diff_fit_max)]

   pylab.annotate("Maximum (%.2f)" % (diff_fit_max,), xy=(gen_max_fit, diff_fit_max),  xycoords='data',
                xytext=(-150, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Fitness difference")

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_maxmin_raw(pop, minimize, filesave=None):
   x = []
   max_y = []
   min_y = []
   std_dev_y = []
   avg_y = []

   for it in pop:
      x.append(it["generation"])
      max_y.append(it["rawMax"])
      min_y.append(it["rawMin"])
      std_dev_y.append(it["rawDev"])
      avg_y.append(it["rawAve"])

   pylab.figure()

   pylab.plot(x, max_y, "g", label="Max raw", linewidth=1.2)
   pylab.plot(x, min_y, "r", label="Min raw", linewidth=1.2)
   pylab.plot(x, avg_y, "b", label="Avg raw", linewidth=1.2)
   pylab.plot(x, std_dev_y, "k", label="Std Dev raw", linewidth=1.2)

   pylab.fill_between(x, min_y, max_y, color="g", alpha=0.1, label="Diff max/min")

   if minimize: raw_max = min(min_y)
   else: raw_max= max(max_y)

   if minimize: gen_max = x[min_y.index(raw_max)]
   else: gen_max = x[max_y.index(raw_max)]

   min_std = min(std_dev_y)
   gen_min_std = x[std_dev_y.index(min_std)]

   max_std = max(std_dev_y)
   gen_max_std = x[std_dev_y.index(max_std)]

   if minimize: annot_label = "Minimum (%.2f)" % (raw_max,)
   else: annot_label = "Maximum (%.2f)" % (raw_max,)


   pylab.annotate(annot_label, xy=(gen_max, raw_max),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.annotate("Min StdDev (%.2f)" % (min_std,), xy=(gen_min_std, min_std),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.annotate("Max StdDev (%.2f)" % (max_std,), xy=(gen_max_std, max_std),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Raw score")
   pylab.title("Plot of evolution identified by '%s' (raw scores)" % (options.identify))

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()


def graph_maxmin_fitness(pop, minimize, filesave=None):
   x = []
   max_y = []
   min_y = []
   avg_y = []

   for it in pop:
      x.append(it["generation"])
      max_y.append(it["fitMax"])
      min_y.append(it["fitMin"])
      avg_y.append(it["fitAve"])

   pylab.figure()
   pylab.plot(x, max_y, "g", label="Max fitness")
   pylab.plot(x, min_y, "r", label="Min fitness")
   pylab.plot(x, avg_y, "b", label="Avg fitness")

   pylab.fill_between(x, min_y, max_y, color="g", alpha=0.1, label="Diff max/min")

   if minimize: raw_max = min(min_y)
   else: raw_max = max(max_y)

   if minimize: gen_max = x[min_y.index(raw_max)]
   else: gen_max = x[max_y.index(raw_max)]

   if minimize: annot_label = "Minimum (%.2f)" % (raw_max,)
   else: annot_label = "Maximum (%.2f)" % (raw_max,)

   pylab.annotate(annot_label, xy=(gen_max, raw_max),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Fitness score")
   pylab.title("Plot of evolution identified by '%s' (fitness scores)" % (options.identify))
   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_errorbars_raw(pop, minimize, filesave=None):
   x = []
   y = []
   yerr_max = []
   yerr_min = []

   for it in pop:
      x.append(it["generation"])
      y.append(it["rawAve"])
      ymax = it["rawMax"] - it["rawAve"]
      ymin = it["rawAve"] - it["rawMin"]
      
      yerr_max.append(ymax)
      yerr_min.append(ymin)

   pylab.figure()
   pylab.errorbar(x, y, [yerr_min, yerr_max], ecolor="g")
   pylab.xlabel('Generation (#)')
   pylab.ylabel('Raw score Min/Avg/Max')
   pylab.title("Plot of evolution identified by '%s' (raw scores)" % (options.identify))
   pylab.grid(True)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_errorbars_fitness(pop, minimize, filesave=None):
   x = []
   y = []
   yerr_max = []
   yerr_min = []

   for it in pop:
      x.append(it["generation"])
      y.append(it["fitAve"])
      ymax = it["fitMax"] - it["fitAve"]
      ymin = it["fitAve"] - it["fitMin"]
      
      yerr_max.append(ymax)
      yerr_min.append(ymin)

   pylab.figure()
   pylab.errorbar(x, y, [yerr_min, yerr_max], ecolor="g")
   pylab.xlabel('Generation (#)')
   pylab.ylabel('Fitness score Min/Avg/Max')
   pylab.title("Plot of evolution identified by '%s' (fitness scores)" % (options.identify))

   pylab.grid(True)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_compare_raw(pop, minimize, id_list, filesave=None):
   colors_list = ["g", "b", "r", "k", "m", "y"]
   index = 0

   pylab.figure()
   
   for it_out in pop:
      x = []
      max_y = []
      min_y = []

      for it in it_out:
         x.append(it["generation"])
         max_y.append(it["rawMax"])
         min_y.append(it["rawMin"])


      if minimize:
         pylab.plot(x, max_y, colors_list[index], linewidth=0.05)
         pylab.plot(x, min_y, colors_list[index], label="Raw min (%s)" % (id_list[index],), linewidth=1.3)
      else:
         pylab.plot(x, max_y, colors_list[index], label="Raw max (%s)" % (id_list[index],), linewidth=1.3)
         pylab.plot(x, min_y, colors_list[index], linewidth=0.05)

      pylab.fill_between(x, min_y, max_y, color=colors_list[index], alpha=0.06,)

      index += 1

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Raw score")
   pylab.title("Plot of evolution identified by '%s' (raw scores)" % ('many',))
   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_compare_fitness(pop, minimize, id_list, filesave=None):
   colors_list = ["g", "b", "r", "k", "m", "y"]
   index = 0

   pylab.figure()
   
   for it_out in pop:
      x = []
      max_y = []
      min_y = []

      for it in it_out:
         x.append(it["generation"])
         max_y.append(it["fitMax"])
         min_y.append(it["fitMin"])

      if minimize:
         pylab.plot(x, max_y, colors_list[index], linewidth=0.05)
         pylab.plot(x, min_y, colors_list[index], label="Fitness min (%s)" % (id_list[index],), linewidth=1.3)
      else:
         pylab.plot(x, max_y, colors_list[index], label="Fitness max (%s)" % (id_list[index],), linewidth=1.3)
         pylab.plot(x, min_y, colors_list[index], linewidth=0.05)

      pylab.fill_between(x, min_y, max_y, color=colors_list[index], alpha=0.06,)

      index += 1

   pylab.xlabel("Generation (#)")
   pylab.ylabel("Fitness score")
   pylab.title("Plot of evolution identified by '%s' (fitness scores)" % ('many',))
   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()


if __name__ == "__main__":
   from pyevolve import __version__ as pyevolve_version
   from pyevolve import __author__ as pyevolve_author

   popGraph = False

   print "Pyevolve %s - Graph Plot Tool" % (pyevolve_version,)
   print "By %s\n" % (pyevolve_author,)
   parser = OptionParser()

   parser.add_option("-f", "--file", dest="dbfile",
                  help="Database file to read (default is 'pyevolve.db').", metavar="FILENAME", default="pyevolve.db")

   parser.add_option("-i", "--identify", dest="identify",
                  help="The identify of evolution.", metavar="IDENTIFY")

   parser.add_option("-o", "--outfile", dest="outfile",
                  help="""Write the graph image to a file (don't use extension, just the filename, default is png format, but you can change using --extension (-e) parameter).""",
                  metavar="OUTFILE")

   parser.add_option("-e", "--extension", dest="extension",
                  help="""Graph image file format. Supported options (formats) are: emf, eps, pdf, png, ps, raw, rgba, svg, svgz. Default is 'png'.""",
                  metavar="EXTENSION", default="png")

   parser.add_option("-g", "--genrange", dest="genrange",
                  help="""This is the generation range of the graph, ex: 1:30 (interval between 1 and 30).""",
                  metavar="GENRANGE")

   parser.add_option("-l", "--lindrange", dest="lindrange",
                  help="""This is the individual range of the graph, ex: 1:30 (individuals between 1 and 30), only applies to heatmaps.""",
                  metavar="LINDRANGE")
  
   parser.add_option("-c", "--colormap", dest="colormap",
                  help="""Sets the Color Map for the graph types 8 and 9. Some options are: summer, bone, gray, hot, jet, cooper, spectral. The default is 'jet'.""",
                  metavar="COLORMAP", default="jet")

   parser.add_option("-m", "--minimize", action="store_true",
                  help="Sets the 'Minimize' mode, default is the Maximize mode. This option makes sense if you are minimizing your evaluation function.", dest="minimize")

   group = OptionGroup(parser, "Graph types", "This is the supported graph types")

   group.add_option("-0", action="store_true", help="Write all graphs to files. Graph types: 1, 2, 3, 4 and 5.", dest="all_graphs")

   group.add_option("-1", action="store_true", help="Error bars graph (raw scores).", dest="errorbars_raw")
   group.add_option("-2", action="store_true", help="Error bars graph (fitness scores).", dest="errorbars_fitness")
   group.add_option("-3", action="store_true", help="Max/min/avg/std. dev. graph (raw scores).", dest="maxmin_raw")
   group.add_option("-4", action="store_true", help="Max/min/avg graph (fitness scores).", dest="maxmin_fitness")
   group.add_option("-5", action="store_true", help="Raw and Fitness min/max difference graph.", dest="diff_raw")

   group.add_option("-6", action="store_true", help="Compare best raw score of two or more evolutions (you must specify the identify comma-separed list with --identify (-i) parameter, like 'one, two, three'), the maximum is 6 items.", dest="compare_raw")
   group.add_option("-7", action="store_true", help="Compare best fitness score of two or more evolutions (you must specify the identify comma-separed list with --identify (-i) parameter, like 'one, two, three'), the maximum is 6 items.", dest="compare_fitness")

   group.add_option("-8", action="store_true", help="Show a heat map of population raw score distribution between generations.", dest="pop_heatmap_raw")
   group.add_option("-9", action="store_true", help="Show a heat map of population fitness score distribution between generations.", dest="pop_heatmap_fitness")


   parser.add_option_group(group)

   (options, args) = parser.parse_args()

   if options.identify and (not options.errorbars_raw
                        and not options.errorbars_fitness
                        and not options.maxmin_raw
                        and not options.maxmin_fitness
                        and not options.diff_raw
                        and not options.all_graphs
                        and not options.compare_raw
                        and not options.pop_heatmap_raw
                        and not options.pop_heatmap_fitness
                        and not options.compare_fitness):
      parser.error("You must choose one graph type !")

   if (not options.identify) or (not options.dbfile):
      parser.print_help()
      exit()

   print "Loading modules...."

   import os.path
   if not os.path.exists(options.dbfile):
      print "Database file '%s' not found !" % (options.dbfile, )
      exit()

   import pylab
   from matplotlib.font_manager import FontProperties
   import matplotlib.cm
   import sqlite3
   import math
   import os

   print "Loading database and creating graph..."

   identify_list = options.identify.split(",")
   identify_list = map(str.strip, identify_list)

   pop = None

   if options.pop_heatmap_raw or options.pop_heatmap_fitness:
      conn = sqlite3.connect(options.dbfile)
      conn.row_factory = sqlite3.Row
      c = conn.cursor()

      if options.genrange:
         genrange = options.genrange.split(":")
         ret = c.execute("select distinct generation from population where identify = ? and generation between ? and ?", (options.identify, genrange[0], genrange[1]))
      else:
         ret = c.execute("select distinct generation from population where identify = ?", (options.identify,))

      generations = ret.fetchall()
      if len(generations) <= 0:
         print "No generation data found for the identify '%s' !" % (options.identify,)
         exit()

      pop = []
      for gen in generations:
         pop_tmp = []

         if options.lindrange:
            individual_range = options.lindrange.split(":")
            ret = c.execute("""
                         select *  from population
                         where identify = ?
                         and generation = ?
                         and individual between ? and ?
                         """, (options.identify, gen[0], individual_range[0], individual_range[1]))
         else:
            ret = c.execute("""
                         select *  from population
                         where identify = ?
                         and generation = ?
                         """, (options.identify, gen[0]))

         ret_fetch = ret.fetchall()
         for it in ret_fetch:
            if options.pop_heatmap_raw:
               pop_tmp.append(it["raw"])
            else:
               pop_tmp.append(it["fitness"])
         pop.append(pop_tmp)

      ret.close()
      conn.close()

      if len(pop) <= 0:
         print "No statistic data found for the identify '%s' !" % (options.identify,)
         exit()

      print "%d generations found !" % (len(pop),)

      popGraph = True


   if len(identify_list) == 1 and not popGraph:
      if options.compare_raw or options.compare_fitness:
         parser.error("You can't use this graph type with only one identify !")

      conn = sqlite3.connect(options.dbfile)
      conn.row_factory = sqlite3.Row
      c = conn.cursor()

      if options.genrange:
         genrange = options.genrange.split(":")
         ret = c.execute("select * from statistics where identify = ? and generation between ? and ?", (options.identify, genrange[0], genrange[1]))
      else:
         ret = c.execute("select * from statistics where identify = ?", (options.identify,))

      pop = ret.fetchall()

      ret.close()
      conn.close()

      if len(pop) <= 0:
         print "No statistic data found for the identify '%s' !" % (options.identify,)
         exit()

      print "%d generations found !" % (len(pop),)
   
   elif len(identify_list) > 1 and not popGraph:
      pop = []
      if (not options.compare_raw) and (not options.compare_fitness):
         parser.error("You can't use many ids with this graph type !")

      conn = sqlite3.connect(options.dbfile)
      conn.row_factory = sqlite3.Row
      c = conn.cursor()
      for item in identify_list:
         if options.genrange:
            genrange = options.genrange.split(":")
            ret = c.execute("select * from statistics where identify = ? and generation between ? and ?", (item, genrange[0], genrange[1]))
         else:
            ret = c.execute("select * from statistics where identify = ?", (item,))
         fetchall = ret.fetchall()
         if len(fetchall) > 0:
            pop.append(fetchall)

      ret.close()
      conn.close()

      if len(pop) <= 0:
         print "No statistic data found for the identify list '%s' !" % (options.identify,)
         exit()

      print "%d identify found !" % (len(pop),)

   if options.errorbars_raw:
      if options.outfile: graph_errorbars_raw(pop, options.minimize, options.outfile + "." + options.extension)
      else: graph_errorbars_raw(pop, options.minimize)

   if options.errorbars_fitness:
      if options.outfile: graph_errorbars_fitness(pop, options.minimize, options.outfile + "." + options.extension)
      else: graph_errorbars_fitness(pop, options.minimize)

   if options.maxmin_raw:
      if options.outfile: graph_maxmin_raw(pop, options.minimize, options.outfile + "." + options.extension)
      else: graph_maxmin_raw(pop, options.minimize)

   if options.maxmin_fitness:
      if options.outfile: graph_maxmin_fitness(pop, options.minimize, options.outfile + "." + options.extension)
      else: graph_maxmin_fitness(pop, options.minimize)

   if options.diff_raw:
      if options.outfile: graph_diff_raw(pop, options.minimize, options.outfile + "." + options.extension)
      else: graph_diff_raw(pop, options.minimize)

   if options.all_graphs:
      all_graph_functions = [graph_errorbars_raw, graph_errorbars_fitness, graph_maxmin_raw,
                             graph_maxmin_fitness, graph_diff_raw]
      if options.outfile:
         parser.error("You can't specify one file to all graphs !")
      
      dirname = "graphs_" + options.identify
      if not os.path.isdir(dirname):
         os.mkdir(dirname)

      for graph in all_graph_functions:
         filename = dirname + "/"
         filename += options.identify + "_" + graph.__name__[6:]
         filename += "." + options.extension
         graph(pop, options.minimize, filename)
      
      print "\n\tDone ! The graphs was saved in the directory '%s'" % (dirname)

   if options.compare_raw:
      if options.outfile: graph_compare_raw(pop, options.minimize, identify_list, options.outfile + "." + options.extension)
      else: graph_compare_raw(pop, options.minimize, identify_list )

   if options.compare_fitness:
      if options.outfile: graph_compare_fitness(pop, options.minimize, identify_list, options.outfile + "." + options.extension)
      else: graph_compare_fitness(pop, options.minimize, identify_list )

   if options.pop_heatmap_raw:
      if options.outfile: graph_pop_heatmap_raw(pop, options.minimize, options.colormap, options.outfile + "." + options.extension)
      else: graph_pop_heatmap_raw(pop, options.minimize, options.colormap)
      
   if options.pop_heatmap_fitness:
      if options.outfile: graph_pop_heatmap_fitness(pop, options.minimize, options.colormap, options.outfile + "." + options.extension)
      else: graph_pop_heatmap_fitness(pop, options.minimize, options.colormap)
