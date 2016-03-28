#!/usr/bin/env python
# coding: utf_8
import sys
#import csv
import codecs
import re

# ヘッダ部分の対訳表
header_dict = {
    '^  <title>Release ([0-9.]+)<': { "skip":1, "str":u'  <title>リリースX.X.X</title>\n' },
    '^  <title>Release Date<': { "skip":1, "str":u'  <title>リリース日</title>\n' },
    '^   This release contains a small number of fixes from ([0-9.]+)':
      { "skip":3, "str":u'このリリースはX.X.Xに対し、各種不具合を修正したものです。X.Xメジャーリリースにおける新機能については、<xref linkend="release-X-X">を参照してください。\n'},
    '^   <title>Migration to Version ([0-9.]+)<': { "skip":1, "str":u'バージョンX.X.Xへの移行\n' },
    '^    A dump/restore is not required for those running ([0-9.]+)X':
      { "skip":1, "str":u'X.X.Xからの移行ではダンプ/リストアは不要です。\n' },
    '^    However, if you are upgrading from a version earlier than':
      { "skip":2, "str":u'しかしながら、X.X.X以前のリリースからアップグレードする場合は、<xref linkend="release-X-X-X">を参>照して下さい。' },
    '^   <title>Changes<': { "skip":1, "str":u'   <title>変更点</title>' }
}


#翻訳文を持つディクショナリリストを作成する

def create_transed_list(orid_dataline,targ_sect1_cnt):
#変数定義部
        sect1_flag=False
        sect1_cnt=0
        para_flag=False
        para_cnt=0
        com_flag=False
        tra_flag=False
        item_flag=False
        trans_block=[]
        trans_dict={}
        trans_list=[]

        trans_dictkey_tmp=""

#for debug
        #fdebug=open('debugdict.txt','w')
        for orid_line_data in orid_dataline:

            last_tra_flag=tra_flag

            if  '<sect1' in orid_line_data:
                sect1_flag=True
                sect1_cnt=sect1_cnt+1

            elif '<itemizedlist>' in orid_line_data:
                item_flag=True

            elif '</itemizedlist>' in orid_line_data:
                item_flag=False

            elif '</sect1>' in orid_line_data:
                sect1_flag=False

            elif '<para>' in orid_line_data: 
                para_flag=True
                if int(targ_sect1_cnt)==sect1_cnt and item_flag :
                      para_cnt=para_cnt+1

            elif '<!--' in orid_line_data: 
                if para_flag :
                    com_flag=True # for debug
                    tra_flag=True

            elif '-->' in orid_line_data: 
                com_flag=False # for debug

            elif '</para>' in orid_line_data: 
                para_flag=False
                tra_flag=False
                trans_dictkey_tmp=""
                in_warn=False


#例えば下記のような翻訳文の場合、(1)がディクショナリKEY
#<para>内((1)を含めて)がディクショナリのVALUE
#     <para>  
#<!--
#      In <filename>contrib/pgcrypto</>, uniformly report decryption failures  .....(1)
#      as <quote>Wrong key or corrupt data</> (Noah Misch)
#-->
#<filename>contrib/pgcrypto</>で、復号失敗を報告するメッセージを<quote>Wrong key or corrupt data</>（誤ったキーまたは不正なデータ）に統一しました。
#(Noah Misch)
#     </para> 
            if sect1_flag  and item_flag and  sect1_cnt==int(targ_sect1_cnt):

#翻訳元側のディクショナリを出力するdebug出力。デバッグの際はここのコメントを外す
#                fdebug.write(orid_line_data.encode('utf-8')
#                if para_flag:
#                    fdebug.write('para_flag true:')
#                if tra_flag :
#                    fdebug.write('tralfag true:')
#                if last_tra_flag:
#                    fdebug.write('lasttarflag true:')

                if para_flag :
                    para_cnt=para_cnt+1
                    if tra_flag :
                        trans_list.append(orid_line_data)

                #<para>内の最後の1行になった時、ディクショナリに書き込む.
                if not tra_flag and  last_tra_flag :
                    trans_dict[trans_list[1]]=trans_list

                   #for dbug
                   # for i in trans_list:
                   #     fdebug.write(i.encode('utf_8'))

                    trans_list=[]

        return trans_dict,para_cnt

#第一引数；コピー元関数　第二引数：コピー先関数
if __name__ == '__main__':
    tracnt=0
    para_cnt=0

    #原文と訳文のディクショナリ
    trans_dict={}
    #何番目のセクションを翻訳するのか
    targ_sect1_cnt=1


    print '=============================================================='
    print "Start merge.py"
    print '=============================================================='

#######################検証フェーズ#######################
#引数を検証する
    if len(sys.argv) == 3 :
       print "MESSAGE:引数の数は 3   通常モードです"
       print ""

    elif  len(sys.argv) == 4 :
       print "MESSAGE:引数の数は 4    翻訳対象の <sect1 を選択できるモードです"
       print "MESSAGE:上から%s番目の<sect1の内容が翻訳されます" % sys.argv[3]
       print ""
       targ_sect1_cnt=int(sys.argv[3])
    else:
        print len(sys.argv)
        print "ERROR:引数の指定が間違っています... ex. ./mergern.py filename1 filename2"
        print "ERROR:or"
        print "ERROR:./mergen.py filename1 filename2  sectcount"
        exit()

#ファイル名を検証する
#第一引数と第二引数はかならずsgmlという名前を含む

    if 'sgml' not in sys.argv[1] :
        print 'ERROR:第一引数の値を確認してください。sgmlファイルである必要があります。第一引数：'
        print sys.argv[1] 
        exit()
 
    if 'sgml' not in sys.argv[2] :
        print 'ERROR:第二引数の値を確認してください。sgmlファイルである必要があります。第二引数：'
        print sys.argv[2] 
        exit()

#######################実行フェーズ#######################

#翻訳対象のファイルをOpen
    targ_data_file = codecs.open(sys.argv[2],'rU',encoding='utf_8')
    targ_dataline = targ_data_file.readlines()

    #f=open('outputfile.sgml','w')
    f=open(sys.argv[2]+'.auto','w')


#翻訳文があるファイルをOpen
    orid_data=codecs.open(sys.argv[1],'rU',encoding='utf_8')
    orid_dataline=orid_data.readlines()

    trans_dict,para_cnt=create_transed_list(orid_dataline,targ_sect1_cnt)

#翻訳対象ファイルのloop開始

    gpara_flag=False
    targflag=False 
    sect1_flag=False
    sect1_cnt=0
    in_warn=False

    skip_count = 0
    trans_text = ""

    for targ_line_data in targ_dataline:
#ここからタグの解析
#ディクショナリのキーになる最初の1文は必ずparaの中にある。
       
        if '<sect1' in targ_line_data:
            sect1_flag=True
            sect1_cnt=sect1_cnt + 1

        if '</sect1>' in targ_line_data:
            sect1_flag=False

        if '</para>' in targ_line_data: 
            targflag=False

        #ここからターゲットsgmlの解析

        if sect1_cnt != targ_sect1_cnt:

            f.write(targ_line_data.encode('utf_8'))

        else:

            # ヘッダ部分の置換処理
            header_trans_flag = False
            for hdk in header_dict.keys():
                if (re.match(hdk, targ_line_data)):
                    trans_text = u"-->\n" + header_dict[hdk]["str"]
                    header_trans_flag = True
                    break
            if header_trans_flag : 
                f.write(u"<!--\n".encode('utf_8'));
                skip_count = header_dict[hdk]["skip"]

            if targ_line_data in trans_dict :
                tracnt=tracnt+1
                trans_dictkey_tmp=targ_line_data

                for i in trans_dict[targ_line_data]:
                    f.write(i.encode('utf_8'))
                targflag=True

            if targflag :
                if targ_line_data not in trans_dict[trans_dictkey_tmp] :
                    if not in_warn :
                        print ""
                        print "WARN:原文と翻訳対象文の<para>内で差がある可能性があります"
                        print "WARN:<para>の開始行 " + trans_dictkey_tmp.encode('utf-8')
                    print "WARN:  対象行       "+targ_line_data.rstrip().encode('utf-8')
                    in_warn=True

            if not targflag:
                f.write(targ_line_data.encode('utf_8')) 

            # ヘッダ部分の置換
            if skip_count >= 0:
                skip_count = skip_count - 1
                if skip_count == 0:
                    f.write(trans_text.encode('utf_8'));
                    trans_text = ""


####################### 終了処理 #######################
print ""
print "MESSAGE:コピー終了"
print ""
print '=========================処理統計============================='
print "<para>タグの数　%s" % para_cnt  #for debug
print "翻訳数　%s" % tracnt
print "出力ファイル名: "+ sys.argv[2]+".auto"
print '=============================================================='
