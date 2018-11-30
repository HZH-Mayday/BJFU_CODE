import seaborn as sns
from matplotlib.font_manager import FontProperties

def seaborn_set(style="husl"):
    '''
    具体解决seaborn不显示中文的问题, 并且设置seaborn的分隔色彩
    :param style: (String) husl, hls, Paired...
                    具体见 https://seaborn.pydata.org/tutorial/color_palettes.html
    '''
    myfont=FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf',size=14)
    sns.set(font=myfont.get_name(), palette=style)