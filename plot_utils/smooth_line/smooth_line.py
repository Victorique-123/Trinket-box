import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

def create_line_plot(
    x_data_list,           # 列表,包含每条线的x值数组
    y_data_list,           # 列表,包含每条线的y值数组
    labels,                # 列表,每条线的图例标签
    title,                 # 图表主标题
    xlabel,                # x轴标签
    ylabel,                # y轴标签
    legend_title,          # 图例标题
    output_filename,       # 输出文件名
    colors=None,           # 可选,自定义颜色列表
    figsize=(10, 7),       # 可选,图表大小
    x_range=None,          # 可选,x轴范围元组 (min, max)
    y_range=None,          # 可选,y轴范围元组 (min, max)
    x_ticks=None,          # 可选,x轴刻度数组
    y_ticks=None,          # 可选,y轴刻度数组
    smooth_factor=200,     # 可选,平滑度(插值点数量)
    font_family=None       # 可选,字体族
):
    # 默认颜色方案 - 复古配色
    default_colors = ['#2C3D55', '#A65D57', '#2E5077', '#9B4B7C', '#3E7C8F', '#2C3D55']
    colors = colors if colors else default_colors

    # 设置字体
    if font_family:
        plt.rcParams['font.family'] = font_family
    else:
        # 使用默认无衬线字体
        plt.rcParams['font.family'] = 'DejaVu Sans'

    # 创建图形对象
    plt.figure(figsize=figsize)
    
    # 添加主标题
    plt.suptitle(title, fontsize=14, fontweight='bold', y=0.95)
    
    # 设置背景样式
    ax = plt.gca()
    ax.set_facecolor('#F8F9FA')
    plt.grid(True, linestyle='--', alpha=0.4, color='#E0E0E0')
    
    # 设置图形整体背景色
    fig = plt.gcf()
    fig.patch.set_facecolor('white')
    
    # 为每条线创建平滑曲线
    for i, (x_data, y_data, label) in enumerate(zip(x_data_list, y_data_list, labels)):
        # 创建更密集的点进行插值
        x_smooth = np.linspace(min(x_data), max(x_data), smooth_factor)
        
        # B-spline插值
        spl = make_interp_spline(x_data, y_data, k=2)
        y_smooth = spl(x_smooth)
        
        # 绘制平滑曲线
        plt.plot(x_smooth, y_smooth, '-', 
                color=colors[i % len(colors)], 
                linewidth=2.5, 
                label=label, 
                alpha=0.9)
        
        # 添加原始数据点
        plt.plot(x_data, y_data, 'o', 
                color=colors[i % len(colors)], 
                markersize=9,
                markeredgecolor='white', 
                markeredgewidth=1.8)
    
    # 设置坐标轴范围
    if x_range:
        plt.xlim(x_range)
    if y_range:
        plt.ylim(y_range)
    
    # 设置刻度
    if x_ticks is not None:
        plt.xticks(x_ticks)
    if y_ticks is not None:
        plt.yticks(y_ticks)
    
    # 添加标签
    plt.xlabel(xlabel, fontsize=12, labelpad=10)
    plt.ylabel(ylabel, fontsize=12, labelpad=10)
    
    # 添加图例
    plt.legend(title=legend_title, 
              loc='upper left', 
              frameon=True, 
              framealpha=0.95,
              edgecolor='#CCCCCC', 
              fancybox=False)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图形
    plt.savefig(output_filename, 
                dpi=300, 
                bbox_inches='tight', 
                pad_inches=0.3)
    plt.close()

# 使用示例
if __name__ == "__main__":
    # 示例数据
    processes = np.array([1, 2, 4])
    speedup_40x40 = np.array([1.000, 1.732, 2.892])
    speedup_80x90 = np.array([1.000, 1.908, 3.601])
    speedup_160x180 = np.array([1.000, 1.971, 3.873])
    
    # 调用函数
    create_line_plot(
        x_data_list=[processes, processes, processes],
        y_data_list=[speedup_40x40, speedup_80x90, speedup_160x180],
        labels=['40×40', '80×90', '160×180'],
        title='MPI Parallel Computation Speedup Analysis',
        xlabel='Number of Processes',
        ylabel='Speedup',
        legend_title='Problem Size',
        output_filename='mpi_speedup_analysis.png',
        x_range=(1, 4.2),
        y_range=(0.8, 4.2),
        x_ticks=np.arange(1, 4.1, 0.5),
        y_ticks=np.arange(1, 4.2, 0.5)
        # font_family='Times New Roman'  # 如果系统安装了Times New Roman，可以取消注释这行
    )
    print("The plot has been saved as 'mpi_speedup_analysis.png'")