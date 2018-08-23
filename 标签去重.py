from w3lib.html import remove_tags
html = '''
<ul>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/41055524.html">
百度云管家如何上传一个文件夹&quest;</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/60152962.html">
百度云同步盘只能同步一个文件夹吗&quest;</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/41055021.html">
百度云管家如何上传一个文件&quest;</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/41496526.html">
百度云管家同步盘的同步文件夹是怎么回事&quest;</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/41810082.html">
百度云同步盘的同步文件夹是怎么回事&quest;</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/62895521.html">
电脑如何设置百度云同步盘的同步文件夹</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/248896.html">
微云同步盘不能同步怎么办&quest; 微云同步盘同步出错解决方法</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/41694151.html">
微云同步盘不能同步怎么办&quest;</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/88460694.html">
百度云管家怎么离线高速BT文件&quest;</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/61962294.html">
Win10如何删除百度云管家盘符</a>               
</li>
	<li class="cat-item cat-item-2">
<a href="https://www.kafan.cn/edu/81962181.html">
百度云免费网盘容量是多少</a>               
</li>

'''
html = remove_tags(html).replace('\n', '').replace('              	', '').strip()
print(html)