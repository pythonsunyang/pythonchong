html_str = '''
<html>
 <head>
  <title>
   如何应对生活中的这些事
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    如何应对生活中的这些事
   </b>
  </p >

  <p>
    <div class='main_content'>
      <div>
        <div class='question'> 你刚刚从洗手间出来， 同事问你‘吃过了吗’</div>
        <div class='answer'> 没呢， 已经做好了， 就等你进去 </div>
      </div>
      <div>
        <div class='question'> 刚刚来的一个同事， 叫做魏长城，你如何和她套近乎 </div>
        <div class='answer'> 学太祖，不上长城非好汉 </div>
      </div>
      <div>
        <div class='question'> 你吃了什么，放屁这么臭 </div>
        <div class='answer'> 享受了就得了，还要配方的啦。 </div>
      </div>
      <div>
        <div class='question'> 今天有小哥哥路上跟我搭讪 </div>
        <div class='answer'> 终于有人识货了， 我都有点怀疑自己了。</div>
      </div>
    </div>
  </p >

 </body>
</html>
'''

import re


class tree_node(object):
    def __init__(self, name, attribute_sm, string):
        self.children = []
        self.name = name
        self.attribute_sm = attribute_sm
        self.string = string

    def add_child(self, child):
        self.children.append(child)

    def print_all_tags(self, level):
        if self.name:
            print('    '*level + self.name)
        else:
            print('    ' * level + self.string)
        for child in self.children:
            child.print_all_tags(level+1)

    def find_elment(self, string):
        target_list = string.split('/')[1:]
        print(target_list)
        return self.find_elment_by_name(target_list)

    def find_elment_by_name(self, target_list):
        ret_list = []
        #if self.name == target_list[0]:
        if len(target_list) == 1:
            if self.name == target_list[0]:
                ret_list.append(self)
        else:
            if self.name == target_list[0]:
                for child in self.children:
                    ret_list_tmp = child.find_elment_by_name(target_list[1:])
                    ret_list += ret_list_tmp
        return ret_list



def HTML(html_str):
    pattern = r'<(/?)(\w+)\s*(.*?)>([^<]*)'
    find_res = re.findall(pattern, html_str)

    tmp_list = []
    tree_simple = None
    for item in find_res:
        #print(item)
        if item[0] == '/':
            #print('这是一个闭合标签')
            if len(tmp_list) != 1:
                del tmp_list[-1]
        else:
            #print('这是一个开始标签')
            tree_simple = tree_node(item[1], item[2], None)
            # string 的标签
            string_tag = tree_node(None, None, item[3])
            tree_simple.add_child(string_tag)
            tmp_list.append(tree_simple)
            if len(tmp_list) == 1:
                print('这是一个html标签')
            else:
                tmp_list[-2].add_child(tmp_list[-1])

    html_tag = tmp_list[0]
    return html_tag
# print(html_tag)
# print(len(tmp_list))

if __name__ == '__main__':
    html_tag = HTML(html_str)
    #html_tag.print_all_tags(0)

    title_tag_list = html_tag.find_elment('/html/body/p/div/div')

    for title_tag in title_tag_list:
        title_tag.print_all_tags(0)



#print(find_res)




