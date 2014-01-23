from drudge.drudge.models import *

from django.core.management.base import BaseCommand

from datetime import datetime
import urllib2
from BeautifulSoup import BeautifulSoup
import os
import sys


class Command(BaseCommand):
    help = "Scrape Drudge every 5 minutes to a db, then run publish.py"
    def handle(self, *args, **options):
        
        now = datetime.now()

        if now.hour<7 or now.hour>=21:
            return

        html = urllib2.urlopen('http://www.drudgereport.com/').read()

        section = html.split('<! TOP LEFT STARTS HERE')[1]
        split = section.split('<!')[0]

        soup = BeautifulSoup(split)
        for link in soup.findAll('a'):
            story = Story.objects.create(url=link['href'],hed=link.text,location='left',time=now)
            print 'left', link['href'], link.text
        
        section = html.split('<! MAIN HEADLINE')[1]
        split = section.split('<!')[0]

        soup = BeautifulSoup(split)
        for link in soup.findAll('a'):
            story = Story.objects.create(url=link['href'],hed=link.text,location='banner',time=now)
            print 'banner', link['href'], link.text
        
        
        section = html.split('<! FIRST COLUMN STARTS HERE')[1]
        split = section.split('<!')[0]

        soup = BeautifulSoup(split)
        for link in soup.findAll('a'):
            print 'col1', link['href'], link.text
            story = Story.objects.create(url=link['href'],hed=link.text,location='col1',time=now)


        section = html.split('<! SECOND COLUMN')[1]
        split = section.split('<!')[0]

        soup = BeautifulSoup(split)
        for link in soup.findAll('a'):
            print 'col2', link['href'], link.text
            story = Story.objects.create(url=link['href'],hed=link.text,location='col2',time=now)


        section = html.split('<! THIRD COLUMN')[1]
        split = section.split('<!')[0]

        soup = BeautifulSoup(split)
        for link in soup.findAll('a'):
            print 'col3', link['href'], link.text
            story = Story.objects.create(url=link['href'],hed=link.text,location='col3',time=now)


        publish_path = sys.path[0] + '/drudge/publish.py'
        print publish_path
        os.system('python %s' % publish_path)

"""
0 	<title>DRUDGE REPORT 2014&#174;</title>
<META HTTP-EQUIV="X-Headline
1 -- 
var timer = setInterval("autoRefresh()", 1000 * 60 * 3);
functio
2 -- 
@media only screen and (max-device-width: 480px) {
html {-webkit
3 --JavaScript Tag  // Intermarkets Website: DrudgeReport // Page: Drudg
4 -- End of JavaScript Tag -->
</center>
<div id="drudgeTopHeadlines">
5  TOP LEFT STARTS HERE><tt><b>
<IMG SRC="http://l2.yimg.com/bt/api/res
6  MAIN HEADLINE><font FACE="ARIAL,VERDANA,HELVETICA"><font size="+7"><I
7 -- Main headlines links END --->
</b></tt>
</div>

<center>
<a hr
8  FIRST COLUMN STARTS HERE>
<center><table CELLPADDING="3" WIDTH="100%
9 --JavaScript Tag  // Website: DrudgeReport // Page: DrudgeReport - Hom
10 -- End of JavaScript Tag -->
<hr>


11     L I N K S    F I R S T    C O L U M N>


<A HREF="http://news.m
12  SECOND COLUMN BEGINS HERE>
<td ALIGN="LEFT" VALIGN="TOP" WIDTH="30%"
13  L I N K S      S E C O N D     C O L U M N>

<A HREF="http://wabcra
14  THIRD COLUMN STARTS HERE>
<td align="center" valign="top" width="3">
15 --JavaScript Tag  // Website: DrudgeReport // Page: DrudgeReport - Hom
16 -- End of JavaScript Tag -->

<hr>


17  L I N K S    A N D   S E A R C H E S     3 R D    C O L U M N>

<a 
18 --JavaScript Tag  // Website: DrudgeReport // Page: DrudgeReport - Hom
19 -- End of JavaScript Tag -->
<hr>

<A HREF="http://news.google.com/
20 -- Page Reloader, Headline Updater, eProof, DRAMini -->
<script type=
21 -- eProof.com end --> 


22 -- Start Quantcast tag -->
<script type="text/javascript" src="http:/
23 -- End Quantcast tag -->

</b></tt>
</TD>
</TR>
</TABLE></center>
24 --	
// ads breaking timer, this restarts timer
if (typeof timer == '
25 -- Copyright 2011 by Drudge Report --!>   

26 -- END -- DO NOT REMOVE THIS LINE --Adrian --!>


"""

"""
0 


1 DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html><h
2 --
	function dra_sideBar(parent) {
		
			return true;
		
	};
	fu
3 --
/****************************************************
 AntiSpambo
4 -- 
var timer = setInterval("autoRefresh()", 1000 * 60 * 3);
functio
5 -- 
@media only screen and (max-device-width: 480px) {
html {-webkit
6 --JavaScript Tag  // Intermarkets Website: DrudgeReport // Page: Drudg
7 -- End of JavaScript Tag -->
</center>
<div id="drudgeTopHeadlines">
8  TOP LEFT STARTS HERE><tt><b>
<A HREF="http://www.cbsnews.com/news/mu
9  MAIN HEADLINE><font FACE="ARIAL,VERDANA,HELVETICA"><font size="+7"><I
10 -- Main headlines links END --->
</b></tt>
</div>

<center>
<a hr
11  FIRST COLUMN STARTS HERE>
<center><table CELLPADDING="3" WIDTH="100%
12 --JavaScript Tag  // Website: DrudgeReport // Page: DrudgeReport - Hom
13 -- End of JavaScript Tag -->
<hr>


14     L I N K S    F I R S T    C O L U M N>


<A HREF="http://news.m
15  SECOND COLUMN BEGINS HERE>
<td ALIGN="LEFT" VALIGN="TOP" WIDTH="30%"
16  L I N K S      S E C O N D     C O L U M N>

<A HREF="http://wabcra
17  THIRD COLUMN STARTS HERE>
<td align="center" valign="top" width="3">
18 --JavaScript Tag  // Website: DrudgeReport // Page: DrudgeReport - Hom
19 -- End of JavaScript Tag -->

<hr>


20  L I N K S    A N D   S E A R C H E S     3 R D    C O L U M N>

<a 
21 --JavaScript Tag  // Website: DrudgeReport // Page: DrudgeReport - Hom
22 -- End of JavaScript Tag -->
<hr>

<A HREF="http://news.google.com/
23 -- Page Reloader, Headline Updater, eProof, DRAMini -->
<script type=
24 -- eProof.com end --> 


25 -- Start Quantcast tag -->
<script type="text/javascript" src="http:/
26 -- End Quantcast tag -->

</b></tt>
</TD>
</TR>
</TABLE></center>
27 --	
// ads breaking timer, this restarts timer
if (typeof timer == '
28 -- Copyright 2011 by Drudge Report --!>   

29 -- END -- DO NOT REMOVE THIS LINE --Adrian --!>

</td>
<td valign="



<BR><BR><BR>


<! MAIN HEADLINE><font FACE="ARIAL,VERDANA,HELVETICA"><font size="+7"><IMG SRC="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRZI0eviOhMFyIO_hMC0lr2Dh3SavTk2pZvXwlK1__e3aBDqy6UHg" width=525><BR><A HREF="http://houston.cbslocal.com/2013/12/18/duck-dynasty-star-a-vagina-is-more-desirable-than-a-mans-anus/">'DUCK DYNASTY' STAR TAKES ON GAYS</A>


</center>
<!-- Main headlines links END --->
</b></tt>
</div>

<center>
<a href="http://www.drudgereport.com/"><img src="http://www.drudgereport.com/i/logo9.gif" border="0" WIDTH="610" HEIGHT="85"></a>
</center><br>

</b></tt>

<! FIRST COLUMN STARTS HERE>
<center><table CELLPADDING="3" WIDTH="100%"><tr>
<td ALIGN="LEFT" VALIGN="TOP" WIDTH="30%"><tt><b>

<IMG SRC="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTtAw9tj80jNLYH0YNmavoDVn5N2mx4LUwnRv2zjMopUVULe1YK" width=200>
<BR><BR>
<A HREF="http://www.usatoday.com/story/theoval/2013/12/18/podesta-gop-jonestown-cult/4109385/"><font color=red>HOPE AND CHANGE '14:  New Obama adviser compares GOP to Jonestown cult...</font></A><BR><BR>
<A HREF="http://cnsnews.com/mrctv-blog/james-beattie/rep-s"""
                                    
