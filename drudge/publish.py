import os
from datetime import date, datetime, timedelta

import psycopg2
import boto
from boto.s3.key import Key

from email.MIMEText import MIMEText
import smtplib

from credentials import *


now = datetime.now()
day = now - timedelta(days=1)
week = now - timedelta(days=7)

if True:
       
    conn_string = "dbname='drudge'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()


    cursor.execute("select min(time), max(time) from drudge_story")
    (firstchecked,lastchecked_raw) = cursor.next()
    firstchecked = firstchecked.strftime("%m/%d/%Y")  
    lastchecked = lastchecked_raw.strftime("%Y-%m-%d %I:%M%p")

    sections = {}
	
    #all time / last week / last day

    section = {'title': 'Minutes per story', 'long': 'The number of minutes a story stayed on Drudge'}

    section['day'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story WHERE time>=%s group by url, outlet order by count(*) desc limit 10", (day,))
    for line in cursor:
        section['day'].append(line)

    section['week'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story WHERE time>=%s group by url, outlet order by count(*) desc limit 10", (week,))
    for line in cursor:
        section['week'].append(line)

    section['all'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story group by url, outlet order by count(*) desc limit 10")
    for line in cursor:
        section['all'].append(line)

    sections['MinPerStory'] = section



    #minutes per outlet
    section = {'title': 'Minutes per outlet', 'long': 'The number of minutes stories stayed up, totaled by outlet'}

    section['day'] = []
    cursor.execute("select outlet, count(*)*5 n from drudge_story  WHERE time>=%s group by outlet order by count(*) desc limit 10", (day,))
    for line in cursor:
        section['day'].append(line)

    section['week'] = []
    cursor.execute("select outlet, count(*)*5 n from drudge_story  WHERE time>=%s group by outlet order by count(*) desc limit 10", (week,))
    for line in cursor:
        section['week'].append(line)

    section['all'] = []
    cursor.execute("select outlet, count(*)*5 n from drudge_story  group by outlet order by count(*) desc limit 10")
    for line in cursor:
        section['all'].append(line)

    sections['MinPerOutlet'] = section



    #stories per outlet
    section = {'title': 'Stories per outlet', 'long': 'The number of different stories from a given media outlet that made Drudge'}

    section['day'] = []
    cursor.execute("select outlet, count(distinct url) n from drudge_story WHERE time>=%s group by outlet order by count(distinct url) desc limit 10", (day,))
    for line in cursor:
        section['day'].append(line)

    section['week'] = []
    cursor.execute("select outlet, count(distinct url) n from drudge_story WHERE time>=%s group by outlet  order by count(distinct url) desc limit 10", (week,))
    for line in cursor:
        section['week'].append(line)

    section['all'] = []
    cursor.execute("select outlet, count(distinct url) n from drudge_story group by outlet order by count(distinct url) desc limit 10")
    for line in cursor:
        section['all'].append(line)

    sections['StoriesPerOutlet'] = section


    #banners per outlet
    section = {'title': 'Banners per outlet', 'long': 'The number of stories from a given outlet that made the main, large banner of Drudge for any period'}

    section['day'] = []
    cursor.execute("select outlet, count(distinct url) n  from drudge_story where location='banner' AND time>=%s group by outlet order by count(distinct url) desc limit 10", (day,))
    for line in cursor:
        section['day'].append(line)

    section['week'] = []
    cursor.execute("select outlet, count(distinct url) n  from drudge_story where location='banner' AND time>=%s group by outlet order by count(distinct url) desc limit 10", (week,))
    for line in cursor:
        section['week'].append(line)

    section['all'] = []
    cursor.execute("select outlet, count(distinct url) n  from drudge_story where location='banner' group by outlet order by count(distinct url) desc limit 10")
    for line in cursor:
        section['all'].append(line)

    sections['BannersPerOutlet'] = section

    #minutes per banner
    section = {'title': 'Minutes per banner', 'long': 'How long a given story stayed in the most prominent slot'}

    section['day'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story where location='banner' AND time>=%s group by url, outlet order by count(*) desc limit 10", (day,))
    for line in cursor:
        section['day'].append(line)

    section['week'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story where location='banner' AND time>=%s group by url, outlet order by count(*) desc limit 10", (week,))
    for line in cursor:
        section['week'].append(line)

    section['all'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story where location='banner' group by url, outlet order by count(*) desc limit 10")
    for line in cursor:
        section['all'].append(line)

    sections['MinPerBanner'] = section


    #examiner stories by minutes
    section = {'title': 'MediaDC stories by minutes', 'long': 'How long MediaDC stories stayed up'}

    section['day'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story where outlet  IN %s AND time>=%s group by url, outlet order by count(*) desc limit 10", (OUTLETS,day))
    for line in cursor:
        section['day'].append(line)

    section['week'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story where outlet IN %s AND time>=%s group by url, outlet order by count(*) desc limit 10", (OUTLETS,week))
    for line in cursor:
        section['week'].append(line)

    section['all'] = []
    cursor.execute("select url, outlet, count(*)*5 n, min(hed) from drudge_story where outlet IN %s group by url, outlet order by count(*) desc limit 10",(OUTLETS,))
    for line in cursor:
        section['all'].append(line)


    sections['WEXByMin'] = section

    #newest
    section = {'title': 'Newest on Drudge', 'long': 'The most recently posted Drudge stories and how long they\'ve been up'}

    section['day'] = []
    cursor.execute("SELECT a.url, a.outlet, b.n, a.hed FROM (SELECT url, outlet, hed FROM drudge_story WHERE time=%s) a INNER JOIN (SELECT url, count(*)*5 n FROM drudge_story GROUP BY url) b ON (a.url=b.url) ORDER BY b.n LIMIT 10", (lastchecked_raw,))
    for line in cursor:
        section['day'].append(line)

    sections['NewestByMin'] = section


    #examiner stories by minutes
    section = {'title': 'MediaDC Drudge hits by month', 'long': ''}

    section['day'] = []
    cursor.execute("select extract(year from time), extract(month from time), outlet, count(distinct url) n from drudge_story WHERE outlet IN %s group by  extract(year from time), extract(month from time), outlet order by  extract(year from time), extract(month from time), outlet", (OUTLETS,))
    for line in cursor:
        section['day'].append(line)


    sections['StoriesByMonth'] = section

   
                                    
    fout = open('index.html','w')
    
    fout.write("""<html><head><title>Drudge Tracker</title></head><style>
.CSSTableGenerator {
	margin:0px;padding:0px;
	box-shadow: 10px 10px 5px #888888;
	border:1px solid #000000;
	
	-moz-border-radius-bottomleft:0px;
	-webkit-border-bottom-left-radius:0px;
	border-bottom-left-radius:0px;
	
	-moz-border-radius-bottomright:0px;
	-webkit-border-bottom-right-radius:0px;
	border-bottom-right-radius:0px;
	
	-moz-border-radius-topright:0px;
	-webkit-border-top-right-radius:0px;
	border-top-right-radius:0px;
	
	-moz-border-radius-topleft:0px;
	-webkit-border-top-left-radius:0px;
	border-top-left-radius:0px;
}.CSSTableGenerator table{
    border-collapse: collapse;
        border-spacing: 0;
	height:100%;
	margin:0px;padding:0px;
}.CSSTableGenerator tr:last-child td:last-child {
	-moz-border-radius-bottomright:0px;
	-webkit-border-bottom-right-radius:0px;
	border-bottom-right-radius:0px;
}
.CSSTableGenerator table tr:first-child td:first-child {
	-moz-border-radius-topleft:0px;
	-webkit-border-top-left-radius:0px;
	border-top-left-radius:0px;
}
.CSSTableGenerator table tr:first-child td:last-child {
	-moz-border-radius-topright:0px;
	-webkit-border-top-right-radius:0px;
	border-top-right-radius:0px;
}.CSSTableGenerator tr:last-child td:first-child{
	-moz-border-radius-bottomleft:0px;
	-webkit-border-bottom-left-radius:0px;
	border-bottom-left-radius:0px;
}.CSSTableGenerator tr:hover td{
	
}
.CSSTableGenerator tr:nth-child(odd){ background-color:#ffaa56; }
.CSSTableGenerator tr:nth-child(even)    { background-color:#ffffff; }.CSSTableGenerator td{
	vertical-align:middle;
	
	
	border:1px solid #000000;
	border-width:0px 1px 1px 0px;
	text-align:left;
	padding:7px;
	font-size:10px;
	font-family:Arial;
	font-weight:normal;
	color:#000000;
}.CSSTableGenerator tr:last-child td{
	border-width:0px 1px 0px 0px;
}.CSSTableGenerator tr td:last-child{
	border-width:0px 0px 1px 0px;
}.CSSTableGenerator tr:last-child td:last-child{
	border-width:0px 0px 0px 0px;
}
.CSSTableGenerator tr:first-child td{
		background:-o-linear-gradient(bottom, #ff7f00 5%, #bf5f00 100%);	background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #ff7f00), color-stop(1, #bf5f00) );
	background:-moz-linear-gradient( center top, #ff7f00 5%, #bf5f00 100% );
	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr="#ff7f00", endColorstr="#bf5f00");	background: -o-linear-gradient(top,#ff7f00,bf5f00);

	background-color:#ff7f00;
	border:0px solid #000000;
	text-align:center;
	border-width:0px 0px 1px 1px;
	font-size:14px;
	font-family:Arial;
	font-weight:bold;
	color:#ffffff;
}
.CSSTableGenerator tr:first-child:hover td{
	background:-o-linear-gradient(bottom, #ff7f00 5%, #bf5f00 100%);	background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #ff7f00), color-stop(1, #bf5f00) );
	background:-moz-linear-gradient( center top, #ff7f00 5%, #bf5f00 100% );
	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr="#ff7f00", endColorstr="#bf5f00");	background: -o-linear-gradient(top,#ff7f00,bf5f00);

	background-color:#ff7f00;
}
.CSSTableGenerator tr:first-child td:first-child{
	border-width:0px 0px 1px 0px;
}
.CSSTableGenerator tr:first-child td:last-child{
	border-width:0px 0px 1px 1px;
}

a { text-decoration: none; color: black; } 
</style></head><body><h3>Drudge Stats -- lukerosiak.info/drudge.html</h3><p>By <a href="www.lukerosiak.info">Luke Rosiak</a>. Monitors <a href="www.drudgereport.com">Drudge</a> every 5 minutes 7am-10pm. Last updated """+lastchecked)


    for table in ['NewestByMin',]: 
        
        section = sections[table]

        fout.write('<h3>'+section['title']+'</h3><p>'+section['long']+'</p><table class="CSSTableGenerator"><tr><th>Story</th><th>Minutes</th></tr>')
        #url, outlet, count(*) n, min(hed) 
        for row in section['day']:
            fout.write('<tr><td><a href="%s">%s (%s)</a></td><td>%s</td></tr>' % (row[0],row[3],row[1],row[2]))

        fout.write('</table>')



    for table in ['StoriesPerOutlet','MinPerOutlet', 'BannersPerOutlet']: 
        
        section = sections[table]

        fout.write('<h3>'+section['title']+'</h3><p>'+section['long']+"""</p><table class="CSSTableGenerator"><tr>
<th colspan="2">Last 24 hours</th>
<th colspan="2">Last 7 days</th>
<th colspan="2">Since %s</th>
</tr>""" % firstchecked)
        for i in range(0,10):
            fout.write("<tr>")
            for c in ['day','week','all']:
                try:
                    line = '<td><a href="http://%s">%s</a></td><td>%s</td>' % (section[c][i][0],section[c][i][0],section[c][i][1])
                except:
                    line = '<td colspan="2"></td>'
                fout.write(line)
            fout.write('</tr>')

        fout.write('</table>')


    for table in ['MinPerStory','MinPerBanner', 'WEXByMin']: 
        
        section = sections[table]

        fout.write('<h3>'+section['title']+'</h3><p>'+section['long']+"""</p><table class="CSSTableGenerator"><tr>
<th colspan="2">Last 24 hours</th>
<th colspan="2">Last 7 days</th>
<th colspan="2">Since %s</th>
</tr>""" % firstchecked)
        #url, outlet, count(*) n, min(hed) 
        for i in range(0,10):
            fout.write("<tr>")
            for c in ['day','week','all']:
                try:
                    line = '<td><a href="%s">%s (%s)</a></td><td>%s</td>' % (section[c][i][0],section[c][i][3],section[c][i][1],section[c][i][2])
                except:
                    line = '<td colspan="2"></td>'
                fout.write(line)
            fout.write('</tr>')

        fout.write('</table>')




    for table in ['StoriesByMonth',]:
        
        section = sections[table]

        fout.write('<h3>'+section['title']+'</h3><p>'+section['long']+'</p><table class="CSSTableGenerator"><tr><th>Month</th><th>Outlet</th><th>Stories</th></tr>')
        #url, outlet, count(*) n, min(hed) 
        for row in section['day']:
            fout.write('<tr><td>%s/%s<td>%s</td><td>%s</td></tr>' % (int(row[0]),int(row[1]),row[2],row[3]))

        fout.write('</table>')



    fout.close()

    conn_s3 = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
    bucket = conn_s3.get_bucket(AWS_BUCKET)
    k = Key(bucket,'drudge.html')
    k.set_contents_from_filename('index.html',policy='public-read')


    emailtext = ''
    cursor.execute("SELECT a.url, a.hed, a.outlet FROM (SELECT url, hed, outlet FROM drudge_story WHERE time=%s AND outlet IN %s) a INNER JOIN (SELECT url, count(*) FROM drudge_story GROUP BY url HAVING count(*)=1) b ON (a.url=b.url)", (lastchecked_raw,OUTLETS))

    for line in cursor:
        emailtext+=line[1]+' '+line[2]+'<br/>'

    if emailtext!='':
        emailtext += EMAIL_SUBSCRIBE
        msg = MIMEText(emailtext,'html')
        msg['From'] = EMAIL_FROM
        msg['To'] = ', '.join( EMAIL_TO )
        msg['Subject'] = 'New Drudge hit'
        s = smtplib.SMTP('localhost')
        s.sendmail(EMAIL_FROM,
EMAIL_TO, msg.as_string())


