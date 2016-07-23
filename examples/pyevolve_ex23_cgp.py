from pyevolve import G2DCartesian, GSimpleGA, Consts, Util, Mutators
import random
import os
from datetime import datetime

PIL_SUPPORT = None
PYDOT_SUPPORT = None

try:
    import numpy as np
except:
    raise ImportError("This example needs numpy module.")

try:
    from PIL import Image, ImageDraw, ImageFilter
    PIL_SUPPORT = True
except:
    PIL_SUPPORT = False
    
try:
    import pydot
    PYDOT_SUPPORT = True
except:
    PYDOT_SUPPORT = False

DIRECTORY = "unities"
INPUT = "./data/input.jpg"
TARGET = "./data/target.jpg"
IMG_WIDTH=608
IMG_HEIGHT=300
    
def gp_blur(src, params):    
    return src.filter(ImageFilter.BLUR)
    
def gp_contour(src, params):    
    return src.filter(ImageFilter.CONTOUR)
    
def gp_detail(src, params):    
    return src.filter(ImageFilter.DETAIL)
    
def gp_edge_enhance(src, params):    
    return src.filter(ImageFilter.EDGE_ENHANCE)
    
def gp_edge_enhance_more(src, params):    
    return src.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
def gp_emboss(src, params):    
    return src.filter(ImageFilter.EMBOSS)
    
def gp_find_edges(src, params):    
    return src.filter(ImageFilter.FIND_EDGES)
    
def gp_smooth(src, params):    
    return src.filter(ImageFilter.SMOOTH)
    
def gp_smooth_more(src, params):    
    return src.filter(ImageFilter.SMOOTH_MORE)
    
def gp_sharpen(src, params):    
    return src.filter(ImageFilter.SHARPEN)
    
def gp_gaussian_blur(src, params):    
    return src.filter(ImageFilter.GaussianBlur(params['pos_int']))
    
def gp_unsharp_mask(src, params):    
    return src.filter(ImageFilter.UnsharpMask(params['pos_int'], 
                                                int(params['percent_int']), 
                                                int(params['pos_float'])))
                                                
def gp_kernel(src, params):
    size = params['kernel_size'][0] * params['kernel_size'][1]
    kernel = params['kernel'][:size]
    return src.filter(ImageFilter.Kernel(params['kernel_size'], 
                                                kernel, 
                                                params['pos_float']))
                                                
def gp_rank_filter(src, params):    
    rank = int(params['img_size_val'] * params['kernel_size_rad'] 
                * params['kernel_size_rad'])
    return src.filter(ImageFilter.RankFilter(params['kernel_size_rad'], 
                                                rank))
                                                
def gp_mode_filter(src, params):    
    return src.filter(ImageFilter.ModeFilter(params['pos_int']))
    
def eval_fitness_mean_diff(chromosome):
    rmse_accum = Util.VectorErrorAccumulator()    
    code = chromosome.getCompiledCode()
    evaluated = np.array(eval(code[0]))
    rmse_accum.append(evaluated, target)
    return rmse_accum.getRMSE()

def store_result(genome, filename):
    if PIL_SUPPORT:
        code = genome.getCompiledCode()
        ev = eval(code[0])
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
               
        ev.save(os.path.join(DIRECTORY, filename))

def store_graph(genome, filename):
    if PYDOT_SUPPORT:
        graph = pydot.Dot(graph_type='graph')
        genome.writeDotGraph(graph)
        graph.write_png(os.path.join(DIRECTORY, filename))
  
def step_callback(engine): 
    step = engine.getCurrentGeneration()
    if step % 100 == 0:              
        best = engine.bestIndividual()
        store_result(best, "%s_%s.png" % (step, best.score))
        store_graph(best, "%s_%s_graph.png" % (step, best.score))                               

def main():    
    pos_int = """ rand_randint(1,17) """
    pos_float = """ rand_uniform(0.1, 16.0) """
    percent_int = """ rand_gauss(100, 40) """
    img_size_val = """ rand_uniform(0, 1) """
    kernel_size = """ rand_choice([(3, 3), (5, 5)]) """
    kernel = """ [rand_uniform(0.1, 2.5) for x in range(0,25) ] """
    kernel_size_rad = """ rand_choice([3, 5]) """
    
    random.seed(datetime.now())
    
    global im, target, tfft
    orig = Image.open(TARGET)    
    target = np.array(orig)     
    im = Image.open(INPUT)    
    im.load()
    
    genome = G2DCartesian.G2DCartesian(32, 3, 1, 1)
    genome.evaluator += eval_fitness_mean_diff
    ga = GSimpleGA.GSimpleGA(genome)
    genome.mutator.set(Mutators.G2DCartesianMutatorNodeParams)
    genome.mutator.add(Mutators.G2DCartesianMutatorNodeInputs)
    genome.mutator.add(Mutators.G2DCartesianMutatorNodeFunction)
    genome.mutator.add(Mutators.G2DCartesianMutatorNodesOrder)
    ga.setPopulationSize(5)
    ga.setGenerations(10000)
    ga.setMultiThreading(True)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setParams(gp_function_prefix = "gp", gp_terminals = ['im'], 
                    gp_args_mapping = { "pos_int" : pos_int,
                                        "pos_float" : pos_float,
                                        "percent_int" : percent_int,
                                        "img_size_val" : img_size_val,
                                        "kernel_size" : kernel_size,
                                        "kernel" : kernel,
                                        "kernel_size_rad" : kernel_size_rad})
    ga.setMutationRate(0.05)
    ga.setElitism(True)
    ga.setSortType(Consts.sortType["raw"])
    ga.stepCallback.set(step_callback)    
    
    ga(freq_stats=100)
    
    best = ga.bestIndividual()  
    store_result(best, "best_%s.png" % (best.score))
    store_graph(best, "best_graph_%s.png" % (best.score))                

if __name__ == "__main__":       
    main()
