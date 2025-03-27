import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import PathPatch, Patch
from matplotlib.path import Path
import numpy as np

def set_axes_color(ax,col, top_col=None):
    for spine in ax.spines.values():
        spine.set_color(col)
    if top_col:
        ax.spines["top"].set_color(top_col) 

def plot_pm10(df_pm10, df_piogge, df_temp, temp_thr=6):
    """Crea il grafico dei livelli di PM10 nel tempo."""
    
    ind_val = np.isfinite(df_pm10["Valore"])

    xx_all = np.array(df_pm10["Data rilevamento"].map(lambda x: x.toordinal()))
    yy_all = np.array(df_pm10["Valore"])

    xx = xx_all[ind_val]
    yy = yy_all[ind_val]

    # Creazione del grafico
    fig, ax = plt.subplots()
    fig.set_size_inches(25 / 365 * len(df_pm10), 8)

    ax.plot(xx, yy, color="#bbb", alpha=1, ls="--", zorder=0.9, lw = 0.75)  # Linea tratteggiata per i valori nulli  
    ax.plot(xx_all, yy_all, color="#999", alpha=1, zorder=1, lw = 0.75)     # Linea continua
    ax.scatter(xx, yy, marker="x", s=10, zorder=1.1, lw=0.75,               # Marker per i valori non nulli
               color=["#444" if i < 50 else "red" for i in yy])             # I valori sopra il limite di legge sono in rosso

    # Creazione del path chiuso
    verts = np.vstack([[xx[0], 0], np.column_stack((xx, yy)) , [xx[-1], 0], [xx[0], 0]])
    path  = Path(verts)
    patch = PathPatch(path, facecolor="none", edgecolor="none", lw=0)

    ax.add_patch(patch)

    # Creazione della mappa di colori basata sui valori di `xx` e `yy`
    cMap = [(         0, '#ffffff'), 
            (       0.1, '#ffffff'), 
            (35/max(yy), '#ffe3ad'), 
            (60/max(yy), '#fe8284'), 
            (         1, '#fe8284')]
    
    customColourMap = LinearSegmentedColormap.from_list("custom", cMap)

    ax.imshow(
        xx.reshape(yy.size, 1),
        cmap = customColourMap,
        interpolation = "gaussian",
        origin = "lower",
        extent = [xx.min(), xx.max(), 0, yy.max()],
        aspect = "auto",
        clip_path = patch,
        clip_on = True
    )

    # Parametri grafici
    side_mrg  = 1
    upper_mrg = 2

    ax.axis([
        min(xx) - side_mrg, 
        max(xx) + side_mrg , 
        0, 
        max(yy) + upper_mrg
    ])

    # Linea orizz. per il limite di legge
    ax.axhline(y = 50, color = "firebrick", ls = "--", lw = 1) 
    ax.text(x = ax.get_xlim()[0]+(ax.get_xlim()[1] - ax.get_xlim()[0]) / 1.5,  
            y = 50 ,  
            s = "Limite di legge: 50 µg/m³",  
            color = "firebrick", 
            fontsize = 12, 
            bbox = dict(facecolor = 'white', alpha = 1, edgecolor = 'white'),
            ha = "center", 
            va = "center")  
    
    set_axes_color(ax, None)
    ax.grid(axis="y", alpha=0.25)

    ax.axes.get_xaxis().set_ticks([])
    ticks = ax.get_yticks()[1:-1]                           # Esclude il primo e l'ultimo tick dell'asse y
    ax.yaxis.set_ticks(ticks)  
    ax.yaxis.set_ticklabels([f"{i} µg/m³" for i in ticks])  # Aggiunge l'unità di misura
    ax.axes.get_yaxis().set_ticks([])

    for tick in ticks:
        ax.axhline(y = tick, color = "grey", alpha=0.25, lw=.5, zorder=-1) 
        ax.text(x = ax.get_xlim()[0]+(ax.get_xlim()[1] - ax.get_xlim()[0]) / 2.5,  
            y = tick ,  
            s = f"{tick} µg/m³",  
            color = "black", 
            alpha=0.45,
            fontsize = 8, 
            bbox = dict(facecolor = 'white', alpha = 1, edgecolor = 'white'),
            ha = "center", 
            va = "center")

    m_lab = [
        "Gennaio",
        "Febbraio",
        "Marzo",
        "Aprile",
        "Maggio",
        "Giugno",
        "Luglio",
        "Agosto",
        "Settembre",
        "Ottobre",
        "Novembre",
        "Dicembre",
    ]

    first_days = xx_all[df_pm10["Data rilevamento"].dt.day == 1]

    for i, f in enumerate(first_days): # Aggiunge le annotazioni in alto
        ax.text(x = f+15,  
            y = 2.5 ,  
            s = m_lab[i],  
            color = "black", 
            alpha=0.45,
            fontsize = 10, 
            ha = "center", 
            va = "top")
        if i>0:
            ax.text(x = f-.5,  
                y = 2.5 ,  
                s = '|',  
                color = "black", 
                alpha=0.45,
                fontsize = 13, 
                ha = "center", 
                va = "top")

    xx_piogge = xx_all[df_piogge["Pioggia"] == 1]
    yy_piogge = np.ones(len(xx_piogge))

    inset_ax = ax.inset_axes([0, -0.05, 1, 0.05], xticks=[], xticklabels=[], yticks=[], yticklabels=[])
    
    inset_ax.axis([
        min(xx) - side_mrg, 
        max(xx) + side_mrg, 
        0, 
        2
    ])
    
    set_axes_color(inset_ax, None, '#eaeaea')
    inset_ax.scatter(xx_piogge, yy_piogge, color="cornflowerblue", alpha=1, s=100, marker="|")
    inset_ax.invert_yaxis()

    xx_temp = xx_all[df_temp["Temperatura minima"] < temp_thr]
    yy_temp = np.ones(len(xx_temp))
    
    inset_ax = ax.inset_axes([0, -0.1, 1, 0.05], xticks=[], xticklabels=[], yticks=[], yticklabels=[])
    
    inset_ax.axis([
        min(xx) - side_mrg, 
        max(xx) + side_mrg, 
        0.6, 
        2
    ])

    set_axes_color(inset_ax, None)
    inset_ax.scatter(xx_temp, yy_temp, color="plum", alpha=1, s=100, marker="|")
    inset_ax.invert_yaxis()

    legend_elements = [Patch(facecolor='cornflowerblue',label='Pioggia'),
                       Patch(facecolor='plum',label='T min < 6 °C')]

    ax.legend(handles=legend_elements, ncols=2, frameon=False, loc='lower right', bbox_to_anchor=(1, -0.15))
    
    #plt.show()
    plt.title('PM10 (Torino, 2024)', loc='center', fontdict={'fontsize': 24, 'fontweight': 'bold'})
    plt.savefig('../img/pm10_torino.pdf', bbox_inches='tight')

def plot_correlation(df, lags, ccf, pvals):

    fig, ax = plt.subplots()

    fig.set_size_inches(8, 4+0.3*len(lags))

    # Grafico a barre
    ax.barh(lags, width=abs(ccf)+ 0.01, color='grey', height=0.05)
    
    # Rimuove gli assi destro e inferiore
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.axis([
        max([0,min(abs(ccf))-max(abs(ccf))*.1]), 
        max(abs(ccf))*1.1, 
        min(lags)-1, 
        max(lags)+1
    ])

    ax.set_yticks(np.arange(min(lags), max(lags) + 1, 1))
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()

    for value, lag in zip(ccf, lags):
        x_pos = abs(value) + 0.01  # Posizione del testo
        text_value = f"{value:.2f}"  # Testo numerico

        # Aggiunge il rettangolo colorato con il valore numerico
        ax.text(x_pos, lag, text_value, 
                va='center', ha='center', fontsize=8, color='white',
                bbox=dict(facecolor='forestgreen', edgecolor='forestgreen', boxstyle='round,pad=0.3'))

        # Aggiunge gli asterischi accanto al rettangolo
        ax.text(x_pos, lag, '      ' + pvals[np.argmax([lags==lag])], va='center', ha='left', fontsize=8, color='#333')

    ax.set_ylabel('Giorni dopo')
    ax.set_xlabel('Cross-Correlation')
    ax.set_title(f'Cross-Correlation {df.columns[0]} vs {df.columns[1]}')
    ax.axes.get_xaxis().set_ticks([])
    ax.invert_yaxis() 

    #plt.show()
    plt.savefig(f'../img/cross_correlation_chart_{df.columns[1]}.pdf', bbox_inches='tight')