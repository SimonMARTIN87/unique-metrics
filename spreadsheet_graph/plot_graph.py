import plotly.plotly as py 
import plotly
import plotly.graph_objs as go
import numpy as np 

plotly.tools.set_credentials_file(username='StephaneINSEAD', api_key='lOQjiZrEQ6mKXDNEo1SX')

def create_group_level_with_Pup(folderName,PoppedUp,started, level1, level2, level3, level4, level5, level6, level7, level8, exported,dates,title) : 
	trace = go.Bar(
	    x=dates,
	    y=PoppedUp,
	    name='PoppedUp'
	)
	trace0 = go.Bar(
	    x=dates,
	    y=started,
	    name='Started'
	)
	trace1 = go.Bar(
	    x=dates,
	    y=level1,
	    name='level1'
	)
	trace2 = go.Bar(
	    x=dates,
	    y=level2,
	    name='level2'
	)
	trace3 = go.Bar(
	    x=dates,
	    y=level3,
	    name='level3'
	)
	trace4 = go.Bar(
	    x=dates,
	    y=level4,
	    name='level4'
	)
	trace5 = go.Bar(
	    x=dates,
	    y=level5,
	    name='level5'
	)
	trace6 = go.Bar(
	    x=dates,
	    y=level6,
	    name='level6'
	)
	trace7 = go.Bar(
	    x=dates,
	    y=level7,
	    name='level7'
	)
	trace8 = go.Bar(
	    x=dates,
	    y=level8,
	    name='level8'
	)
	trace9 = go.Bar(
	    x=dates,
	    y=exported,
	    name='Exported'
	)

	data = [trace,trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace9, trace8]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='completion level',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)

	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name, sharing='private')

def create_group_level_wout_Pup(folderName,started, level1, level2, level3, level4, level5, level6, level7, level8, exported,dates,title) : 

	trace0 = go.Bar(
	    x=dates,
	    y=started,
	    name='Started'
	)
	trace1 = go.Bar(
	    x=dates,
	    y=level1,
	    name='level1'
	)
	trace2 = go.Bar(
	    x=dates,
	    y=level2,
	    name='level2'
	)
	trace3 = go.Bar(
	    x=dates,
	    y=level3,
	    name='level3'
	)
	trace4 = go.Bar(
	    x=dates,
	    y=level4,
	    name='level4'
	)
	trace5 = go.Bar(
	    x=dates,
	    y=level5,
	    name='level5'
	)
	trace6 = go.Bar(
	    x=dates,
	    y=level6,
	    name='level6'
	)
	trace7 = go.Bar(
	    x=dates,
	    y=level7,
	    name='level7'
	)
	trace8 = go.Bar(
	    x=dates,
	    y=level8,
	    name='level8'
	)
	trace9 = go.Bar(
	    x=dates,
	    y=exported,
	    name='Exported'
	)

	data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace9, trace8]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='completion level',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)

	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename= folderName+'/'+name, sharing='private')

def create_group_sentinel_CV(folderName,send_cv,opened_cv,upload_cv,export_cv,dates,title) : 
	trace0 = go.Bar(
	    x=dates,
	    y=send_cv,
	    name='send Email for CV'
	)
	trace1 = go.Bar(
	    x=dates,
	    y=opened_cv,
	    name='open Email for CV'
	)
	trace2 = go.Bar(
	    x=dates,
	    y=upload_cv,
	    name='upload CV'
	)
	trace3 = go.Bar(
	    x=dates,
	    y=export_cv,
	    name='export CV'
	)

	data = [trace0, trace1, trace2, trace3]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='Number by sentinel',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename= folderName+'/'+name,sharing='private')


def create_group_sentinel_reminder(folderName, reminder1, reminder2, reminder3,returned,recover,dates,title) : 
	trace4 = go.Bar(
	    x=dates,
	    y=reminder1,
	    name='reminder 1'
	)
	trace5 = go.Bar(
	    x=dates,
	    y=reminder2,
	    name='reminder 2'
	)
	trace6 = go.Bar(
	    x=dates,
	    y=reminder3,
	    name='reminder 3'
	)
	trace7 = go.Bar(
	    x=dates,
	    y=returned,
	    name='return'
	)
	trace8 = go.Bar(
	    x=dates,
	    y=recover,
	    name='recover'
	)

	data = [trace4, trace5, trace6, trace7, trace8]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='Number by sentinel',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')

def create_group_nps(folderName,star1, star2, star3, star4, star5,dates,title) : 

	trace1 = go.Bar(
	    x=dates,
	    y=star1,
	    name='1 star'
	)
	trace2 = go.Bar(
	    x=dates,
	    y=star2,
	    name='2 stars'
	)
	trace3 = go.Bar(
	    x=dates,
	    y=star3,
	    name='3 stars'
	)
	trace4 = go.Bar(
	    x=dates,
	    y=star4,
	    name='4 stars'
	)
	trace5 = go.Bar(
	    x=dates,
	    y=star5,
	    name='5 stars'
	)

	data = [trace1, trace2, trace3, trace4, trace5]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='Number of stars',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')

def create_line(folderName,dates, y, title) :
	trace = go.Scatter(
    x = dates,
    y = y
    )
	layout = go.Layout(
	    title=title,
	    yaxis=dict(
        title='Number of conversations',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	data = [trace]
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')

def create_group_sessions(folderName,duration,welcomingQuestion,whyMcDonalds,satisfactionQuestion,satisfactionQuestionReply,unhappyClientQuestionReply,dates, title) : 
	trace1 = go.Bar(
	    x=dates,
	    y=duration,
	    name='Duration'
	)
	trace2 = go.Bar(
	    x=dates,
	    y=welcomingQuestion,
	    name='welcomingQuestion'
	)
	trace3 = go.Bar(
	    x=dates,
	    y=whyMcDonalds,
	    name='whyMcDonalds'
	)
	trace4 = go.Bar(
	    x=dates,
	    y=satisfactionQuestion,
	    name='satisfactionQuestion'
	)
	trace5 = go.Bar(
	    x=dates,
	    y=unhappyClientQuestionReply,
	    name='unhappyClientQuestionReply'
	)

	data = [trace1, trace2, trace3, trace4, trace5]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='Time in seconds per opened questions',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')


def create_group_nbconv(folderName,weekday, weekend,dates, title) : 
	trace1 = go.Bar(
	    x=dates,
	    y=weekday,
	    name='Number of conversations  - weekday'
	)
	trace2 = go.Bar(
	    x=dates,
	    y=weekend,
	    name='Number of conversations  - weekend'
	)

	data = [trace1, trace2]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='Number of conversations',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')

def create_group_nbconv1(folderName,y,dates, title) : 
	trace1 = go.Bar(
	    x=dates,
	    y=y,
	    name='Number of conversations - weekday'
	)

	data = [trace1]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='Number of conversations',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')


def create_group(folderName,mobile,desktop, x, title) : 
	trace1 = go.Bar(
	    x=x,
	    y=mobile,
	    name='Mobile'
	)
	trace2 = go.Bar(
	    x=x,
	    y=desktop,
	    name='Desktop'
	)

	data = [trace1, trace2]
	layout = go.Layout(
	    barmode='group',
	    title=title,
	    yaxis=dict(
        title='Number',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    )
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')


