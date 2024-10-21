import sys
from jinja2 import Template
import html as h
import matplotlib.pyplot as plt
import csv


def main():
    fr=open('data.csv','r')
    csvread=csv.reader(fr)
    header=next(csvread)
    rows=[]
    for r in csvread:
        rows.append(r)
    if len(sys.argv)>1:
        if sys.argv=='-s':
            Temp=stutemp(header,rows)
        elif sys.argv=='-c':
            temp=courtemp(rows)
    else:
        temp=wrongtemp()
    temple=Template.render()
    fw=open('output.html','w')
    fw.write(temple)
    fw.close()
    fr.close()

def stutemp(header,rows):
    stuid=sys.argv[2]
    value=0
    for row in rows:
        if row[0]==stuid:
            value+=int(row[2])
    if value==0:
        temp=wrongtemp()
    else:
        temp=h.html(
            h.head(
                h.title('Student Data')
            ),h.body(h.h1('Student Details'),
                h.table(border='1',
                children=[
                    h.tr(
                        h.td(cell) for cell in header
                    ),
                    (h.tr(
                        h.td(cell) for cell in row
                    ) for row in rows if row[0]==stuid
                    ),
                    h.tr(
                        h.td(columnspan='2'),h.td('Total Marks'),h.td(value)
                    )
                ]
                )
            )
        )
    return temp

def courtemp(rows):
    cid=sys.argv[2]
    value=0
    max=0
    data={}
    for row in rows:
        if int(row[1])==int(cid):
            i=int(row[2])
            if (i not in data.keys()):
                data[i]=1
            else:
                data[i]+=1
            value+=i
            if i>max:
                max=i
    avg=value/len(rows)
    if value==0:
        temp=wrongtemp()
    else:
        courses=list(data.keys())
        values=list(data.values())
        fig=plt.figure(figsize=(10,5))
        plt.bar(courses,values)
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        fig.savefig('my_mplt.png')
        temp=h.html(
            h.head(
                h.title('Course Data')
            ),
            h.body(
                h.h1('Course Details'),
                h.table(border='1',
                children=[h.tr(
                    h.td('Average Marks'),h.td('Maximum Marks')
                ),
                h.tr(
                    h.td(avg),h.td(max)
                )

                ]

                )
            )
        )
    return temp
def wrongtemp():
    temp=h.html(
        h.head(
            h.title('Wrong Input')
        ),
        h.body(
            h.p('Something went wrong')
        )
    )
    return temp