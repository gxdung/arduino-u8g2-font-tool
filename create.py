#   
#                  Arduino U8G2 字库生成器    
#        
#                  作者：乐乐龙果冻（gxdung）
#            是只混兽圈的龙龙ww 欢迎关注B站/抖音/小红书
#
#         有任何问题请通过 GitHub Issue 或 B站私信 反馈
#            GitHub：https://github.com/gxdung
#
#--------------------------------------------------------------------------
#
#    本工程系 Gitee 平台 @gastonfeng 的 u8g2_fontmaker 重构项目
#    您可以通过本工具生成 Map、BDF 文件来创建属于您自己的 U8g2 字体字库
#
#--------------------------------------------------------------------------
#
#    项目参考
#    1、bdfconv 命令行生成器：https://stncrn.github.io/u8g2-unifont-helper/
#    2、u8g2：https://github.com/olikraus/u8g2
#    3、u8g2字体懒人脚本工具：https://gitee.com/kaikong/u8g2_fontmaker/tree/main
#   
#

#  0、项目依赖，请检查以下模块是否存在 （如否请通过 pip install 命令安装）

import os, re, pathlib, subprocess, shutil, chardet

#  1、设置字体名称与大小 (路径为 /font 文件夹下)
FontFile  = "PingFang_R.ttf"  # TTF 字体文件名
FontName  = "PingFang_R"  # 字体名称
# FontFile  = "WenQuanDianZhenZhengHei.ttf"  # TTF 字体文件名
# FontName  = "WQYReg"  # 字体名称
FontSizes = [14]  # 字体大小

#  2、字库模式：请配置 StrStatus 变量
#  0：自定义字库 txt格式   1：自定义字库 map格式 

StrStatus = 0     # 字库模式

#  3、设置字库 (路径为 /map 文件夹下)
#  可使用默认字库，请将 furry 修改为以下值
#  chinese1  chinese2  chinese3 
#  gb2312    gb2312a   gb2312b 
StrFile  = "furry" # 字库文件名


#  ********** 以下变量及代码请勿修改 **********
#
#  4、依赖文件配置
MapArray = ["chinese1","chinese2", "chinese3", "gb2312", "gb2312a", "gb2312b"]
Folders  = ["bdf", "font", "code", "map", "tools"]

#  5、路径配置
path = str(pathlib.Path(__file__).parent.resolve())  # 获取当前路径
bdfpath  = path + "\\" + "bdf"
codepath = path + "\\" + "code"
fontpath = path + "\\" + "font"
mappath  = path + "\\" + "map"
toolpath  = path + "\\" + "tools"

#  6、版本号（后续版本添加自动更新）
ver = "1.0.1 (221023)"

#  7、程序部分
#
#  a. 控制台输出字体颜色
class color: 
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    HIGHLIGHT ='\033[1m'

#  b. 版本号输出
def version():
    print("\n - 当前版本：Ver " + ver + "\n")

#  c. 程序初始化
def progstart():
    print(color.BOLD + "\n ------------  Arduino U8g2 字库生成器 （GitHub：gxdung 乐乐龙果冻）  -----------" + color.END)
    version()
    checkFolders()
    checkFiles()
    checkTool()

#  d. 程序结束 / 运行完毕
def progend(): # 结束函数
    print("\n -------------------------------- 程序执行完毕 ---------------------------------- ")
    print(color.BOLD + "\n ------------  Arduino U8g2 字库生成器 （GitHub：gxdung 乐乐龙果冻）  ----------- \n" + color.END)
    exit()

#  e. 检查：目录完整性
def checkFolders():         
    folnum = len(Folders)   # 数组元素个数
    const = 0               # 计数器

    for folder in Folders:
        const += 1
        if os.path.exists(path + "\\" + folder) == 1:
            if(const == folnum):
                print(color.GREEN + " - a. 目 录 检 查 ：通过" + " (" + str(const) + "/" + str(folnum) + ")"+color.END)
        else:
            os.mkdir(path + "\\" + folder)
            print(color.YELLOW +" - a. 目 录 检 查 ：未通过，但已创建 " + folder + " 文件夹" + color.END)

#  f. 检查：内置字库与字体文件完整性
def checkFiles():           

    Fonts = [FontFile]
    fontnum = len(Fonts)     # 字体文件个数
    mapnum = len(MapArray)   # map文件个数
    const = 0                # 计数器

    for file in Fonts:
        const += 1
        if os.path.exists(fontpath + "\\" + file) == 1:
            if(const == fontnum):
                print(color.GREEN +" - b. 字体文件检查：通过" + " (" + str(const) + "/" + str(fontnum) + ")" + color.END)

        else:
            print(color.RED +" - b. 字体文件检查：不存在（" + file + "）" + color.END)
            progend()

    const = 0
    for maps in MapArray:
        const += 1
        if os.path.exists(mappath + "\\" + maps + ".map") == 1:
            if(const == mapnum):
                print(color.GREEN +" - c. 字库文件检查：通过" + " (" + str(const) + "/" + str(mapnum) + ")" + color.END)
        else:
            print(color.RED +" - c. 字库文件检查：异常 " + maps + ".map" + " (" + str(const) + "/" + str(mapnum) + ")"+ color.END)
            progend()
    const = 0

#  g. 检查：自定义字库（TXT）是否存在
def checkOwnTxt():
    if os.path.exists(mappath + "\\" + StrFile + ".txt") == 1:
        print(color.GREEN +" - e. 自定义字库 (TXT)： 存在" + color.END)
    else:
        print(color.RED + " - e. 自定义字库 (TXT)： 不存在, 请检查" + color.END)
        progend()

#  i. 检查：自定义字库（MAP）是否存在
def checkOwnMap():
    if os.path.exists(mappath + "\\" + StrFile + ".map") == 1:
        print(color.GREEN +" - e. 内置字库 (MAP)： 存在" + color.END)
    else:
        print(color.RED + " - e. 内置字库 (MAP)： 不存在, 请检查" + color.END)
        progend()

#  j. 子程序：UTF-8 转 Unicode
def utf8_uni(str):
    Word,Uni,word1=[],[],[]
    for word in str:
        Word.append(word)
        # 正则表达式 匹配A-Z a-z 0-9 特殊符号 空格 换行符
        r = re.compile(r'^[a-zA-Z0-9\x21-\x7e\s\n]') 
    for word in Word:
        result = r.match(word)
        if result != None:
            temp = result.group()
            word1.append(temp)
            temp = hex(ord(word))[2:]
            temp = "\\u00" + temp
            Uni.append(temp)
        else:
            temp = word.encode('unicode_escape')
            Uni.append(temp)
    print(color.HIGHLIGHT + color.PURPLE + '\n - f. 自定义字库 (TXT) 内容 -----------------------------------------------------' + color.END)
    print(Word)
    print(color.HIGHLIGHT + color.CYAN + '\n - g. 原始 Unicode 内容 ---------------------------------------------------------' + color.END)
    print(Uni)
    return(Uni)

#  k. 子程序：TXT 转换成 MAP 文件
def txt2Map():
    #  读取自定义字库（TXT）文件
    txtfile = open(mappath + "\\" + StrFile + ".txt","r",encoding='utf8')
    txtdata = str(txtfile.read())
    #  生成原始 Unicode 内容
    unicode = utf8_uni(txtdata)
    txtfile.close()
    #  生成临时文件 写入后再进行预处理
    temptxt = open(mappath + "\\" + "temp.txt","w",encoding='UTF-8')
    temptxt.write(str(unicode).replace('\\\\u','\\u',-1)) # 替换 “\\u” 为 “\u”
    temptxt.close()
    temptxt = open(mappath + "\\" + "temp.txt","r",encoding='utf8') # 读取文件
    temptxt = str(temptxt.read()) 
    #  预处理 Unicode
    temptxt = temptxt.replace('[','',-1)
    temptxt = temptxt.replace(']','',-1)
    temptxt = temptxt.replace('b\'\\u','\\u',-1)
    temptxt = temptxt.replace('\'','',-1)
    temptxt = temptxt.replace(' ','',-1)
    temptxt = temptxt.replace('\\u','$',-1)

    print(color.HIGHLIGHT + color.YELLOW + '\n - h. 处理后 Unicode 内容 -------------------------------------------------------' + color.END)
    print("32-128," + temptxt.upper())
    os.remove(mappath + "\\" + "temp.txt")

    # 操作 map 文件
    txtfile = open(mappath + "\\" + StrFile + ".map","w",encoding='utf8')

    # 32-128 为 ASCII范围，包含所有字母数字及符号
    txtfile.write("32-128,\n" +temptxt.upper()) 
    txtfile.close()
    print(color.HIGHLIGHT + color.GREEN + '\n - i. 自定义字库 (MAP) : 已生成' + color.END)

#  l. 检查：依赖文件完整性
def checkTool():
    tool=["bdfconv.exe","header1.txt","header2.txt","otf2bdf.exe"]
    const = 0
    for tools in tool:
        if os.path.exists(toolpath + "\\" + tools) == 1:
            const += 1
            if (const == len(tool)):
                print(color.GREEN +" - d. 项目依赖文件：存在" + " (" + str(const) + "/" + str(len(tool)) + ")" + color.END)
        else:
            print(color.RED + " - d. 项目依赖文件： 不存在, 请检查 (" + tools +")" + color.END)
            progend()
    
#  m. TTF 转换成 BDF 字库
def ttf2Bdf():
    print(color.BOLD + color.BLUE + "\n - j. 开始转换BDF文件 ( 调用CMD )" + color.END)
    
    # otf2bdf CMD命令说明
    # -r 设置水平与垂直分辨率  -p 设置所需的像素大小 -o 输出文件
    count = 0  # 计数器

    for px in FontSizes:
        msgl = []  # CMD 控制台输出    
        count += 1 

        # CMD 命令
        cmd1 = "cd " + str(toolpath)
        cmd2 = "otf2bdf -r 100 -p "+ str(px) + " -o "+ str(FontName) +"_" + str(px)+".bdf " + str(fontpath) + "\\" + FontFile
        
        print(color.BLUE + " - 当前CMD命令: " + color.END + cmd1 + "\n                "+ cmd2)
        # CMD 调用
        cmd = subprocess.Popen(cmd1+"&&"+cmd2, shell=True, stdout=subprocess.PIPE)
        msg = cmd.stdout.readline().decode(encoding="gbk")
        msgl.append(msg)

        cmd.wait()
        cmd.stdout.close()
        if(msg==""):
            print(color.GREEN + " - CMD 成功执行: " + "已生成 " + str(px) + "Px 字库" + color.END + " ("+ str(count) + "/" + str(len(FontSizes)) +")"+ "\n")
            shutil.move(str(toolpath) + "\\" + str(FontName) +"_" + str(px)+".bdf", str(bdfpath) + "\\" + str(FontName) +"_" + str(px)+".bdf") # 移动文件
        else:
            print(color.RED + " - CMD 执行异常: " + msgl[0] + " ("+ str(count)  + "/" + str(len(FontSizes)) +")" + color.END + "\n")
            progend()

    count = 0
    print(color.BOLD + color.GREEN + " - BDF 文件成功生成" + color.END)       

#  n. 生成 C 源代码
def sourceCode():
    print(color.BOLD + color.PURPLE + "\n - k. 开始生成 C 语言源文件" + color.END)
    count = 0  # 计数器
    for px in FontSizes:
        count += 1
        msgl = []  # CMD 控制台输出
        cmd1 = "cd " + str(toolpath)

        # bdfconv 命令行说明
        # -b <n> 字体构建模式，0：比例，1：公共高度，2：等宽，3：8的倍数
        # -f <n> 字体格式，0：ucglib 字体，1：u8g2 字体，2：u8g2 未压缩的8x8 字体（强制-b 3）
        # -M 'mapfile' 从文件 'mapfile' 读取 Unicode ASCII 映射
        # -o <file> C 输出文件
        # -n <name> C 标识符（字体名称）
        # 其他说明：https://clz.me/u8g2-bdfconv/

        cmd2 = "bdfconv -b 0 -f 1 -M"+ str(mappath) + "\\" + str(StrFile) + ".map " + "-n " + str(FontName) + "_" + str(px) + " -o "+ str(codepath) + "\\" + str(FontName) + "_" + str(px) + ".c " + str(bdfpath) + "\\" + str(FontName) + "_" + str(px) + ".bdf"

        print(color.BLUE + " - 当前CMD命令: " + color.END + cmd1 + "\n                "+ cmd2)

        # CMD 调用
        cmd = subprocess.Popen(cmd1+"&&"+cmd2, shell=True, stdout=subprocess.PIPE)
        msg = cmd.stdout.readline().decode(encoding="gbk")
        msgl.append(msg)

        cmd.wait()
        cmd.stdout.close()

        if(msg==""):
            print(color.GREEN + " - CMD 成功执行: " + "已生成 " + str(px) + "Px C 文件" + color.END + " ("+ str(count) + "/" + str(len(FontSizes)) +")"+ "\n")
        else:
            print(color.RED + " - CMD 执行异常: " + str(msgl[0]) + " ("+ str(count)  + "/" + str(len(FontSizes)) +")" + color.END + "\n")

    count = 0

#  o. 操作 C 源代码
def editCode():
    print(color.BOLD + color.PURPLE + "\n - l. 开始处理 C 语言源文件" + color.END + "\n")
    count = 0  # 计数器
    error = 0
    for px in FontSizes:
        count += 1
        cpath = str(codepath) + "\\" + str(FontName) + "_" + str(px) + ".c"
        if os.path.exists(cpath) == 1:
            cfile = open(cpath,"r+",encoding='utf8',errors="ignore")
            cdata = cfile.read()
            cfile.close()
            cfile = open(cpath,"w+",encoding="utf-8")
            cfile.seek(0, 0)
            headcode = "\n #include " + "\"" +str(FontName) + "_" + str(px) + ".h" + "\""
            cfile.write(headcode + "\n" + "\n" + str(cdata))
            cfile.close()
            print(color.GREEN + " - 已处理：" + str(px) + "Px C 文件" + color.END + " ("+ str(count) + "/" + str(len(FontSizes)) +")")
        else:
            print(color.RED + " - 文件不存在：" + str(px) + "Px C 文件" + color.END + " ("+ str(count) + "/" + str(len(FontSizes)) +")")
            error += 1
    
    if error>=0:
        print(color.BOLD + color.YELLOW + "\n - Warning: C 语言源文件写入失败或不存在" + " ("+ str(error) + "/" + str(len(FontSizes)) +")"+ color.END + "\n")
    else:
        print(color.BOLD + color.GREEN + "\n - Success: C 语言源文件处理完成" + color.END + "\n")

#  p. 生成 C 语言 Header 代码
def createH():
    print(color.BOLD + color.CYAN + "\n - m. 开始处理 C 语言头文件" + color.END + "\n")
    count = 0  # 计数器
    headpath1 = toolpath + "\\header1.txt"
    headpath2 = toolpath + "\\header2.txt"
    head1 = open(headpath1,"r",encoding='UTF-8')
    head2 = open(headpath2,"r",encoding='UTF-8')
    h1 = head1.read()
    h2 = head2.read()
    head1.close()
    head2.close()

    for px in FontSizes:
        count += 1
        fontname = str(FontName) + "_" + str(px)
        codetemp = "#ifndef _" + fontname.upper() + "_H"
        codetemp = codetemp + "\n" + "#define _" + fontname.upper() + "_H"
        codetemp = codetemp + "\n" + str(h1)
        codetemp = codetemp + "\n" +"extern const uint8_t " + fontname + "[] U8G2_FONT_SECTION(\"" + fontname + "\");"
        codetemp = codetemp + "\n" + "\n" + str(h2)

        htemp = open(codepath + "\\" + fontname + ".h","w",encoding='UTF-8')
        htemp.write(codetemp)
        htemp.close()

        print(color.GREEN + " - 已生成 C Header 文件" + " ("+ str(count) + "/" + str(len(FontSizes)) +")" + color.END)
    
    print(color.BOLD + color.GREEN + " - 程序执行完毕，请检查。" + color.END)

#  p. 模式判断
def modeSelect():
    if StrStatus == 0:
        print("\n ----------------------- " + color.BLUE + "当前模式：0、自定义字库 (TXT) "+ color.END + "--------------------------\n")
        checkOwnTxt()
        txt2Map()
        ttf2Bdf()
        sourceCode()
        editCode()
        createH()
    else:
        print("\n ----------------------- " + color.RED + "当前模式：1、内置字库 (MAP) "+ color.END + "--------------------------\n")
        checkOwnMap()
        ttf2Bdf()
        sourceCode()
        editCode()
        createH()


progstart()
modeSelect()
progend()


