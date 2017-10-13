import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud

a = 'this is a wordcloud show'
wc = WordCloud().generate(a)
wc.to_file('wc.jpg')

plt.imshow(wc)
plt.axis('off')
plt.savefig('plt.png')
