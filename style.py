from cycler import cycler
def ownStyle(mtl):
    mtl.rcParams['axes.linewidth']=1 #outer line thickness
    mtl.rcParams['axes.edgecolor']='#5D2E46'
    mtl.rcParams['axes.facecolor']='#F7EEED'
    mtl.rcParams['figure.facecolor']='#F7EEED'
    mtl.rcParams['xtick.color']='#5D2E46'
    mtl.rcParams['ytick.color']='#5D2E46'
    mtl.rcParams['axes.labelcolor']='#5D2E46'
    try:
        mtl.rcParams['axes.color_cycle']=['#35526D','#AD484C','#5caab7','#69B1B5','#9E807E']
    except KeyError:
        pass
        #mtl.rcParams['axes.prop_cycle': cycler('color', ['#35526D','#AD484C','#5caab7','#69B1B5','#9E807E'])]
