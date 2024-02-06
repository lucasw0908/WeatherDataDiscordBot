import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import logging
from typing import Any

log = logging.getLogger(__name__)

def save_plot_data(data: dict[str:list[Any]], title: str="No Title", xlabel: str="X", ylabel: str="Y", percentage_mode: bool=False, gif: bool=True) -> None:
    """data = {X:[...], Y:[...]}"""
    
    if len(data["X"]) != len(data["Y"]): 
        log.warning("Wrong data length.")
        return None
    
    fontdict = dict(
        fontsize=16,
        family="Microsoft JhengHei",
        weight="bold",
        style="italic"
    )
    
    fig, ax = plt.subplots()

    ax.set_title(title, fontdict=fontdict)
    ax.set_xlabel(xlabel, fontdict=fontdict)
    ax.set_ylabel(ylabel, fontdict=fontdict)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d:%H"))
    
    if not gif:
        ax.plot_date(mdates.date2num(data["X"]), data["Y"], fmt="ro", xdate=True)
        fig.savefig("data.png")
        
    else:
        ax.set_ylim(0, int(100 if percentage_mode else max(data["Y"])+10))

        x, y = [], []

        def run(frames):
            
            x_point = data["X"][int(frames)]
            y_point = data["Y"][int(frames)]
            
            x.append(x_point)
            y.append(y_point)
            
            dates = mdates.date2num(x)
            
            #line.set_data(dates, y)
            ax.plot_date(dates, y, fmt="ro", xdate=True)
        
        ani = animation.FuncAnimation(fig, run, frames=len(data["X"]), interval=30, repeat=False)
        
        ani.save("data.gif", writer="pillow", fps=10)
        
    plt.close()
    plt.clf()