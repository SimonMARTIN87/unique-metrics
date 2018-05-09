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

def create_multiple_lines(folderName, dates, matrix, title) :
	data = []
	for line in matrix.keys() :
		trace = go.Scatter(
			x = dates,
			y = matrix[line],
			mode = 'lines',
			name = line,
			line = dict(shape='spline')
		)
		data.append(trace)
	layout = go.Layout(
		title=title,
		yaxis = dict(title='% of Conversion')
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')	

def create_multiple_perc_lines(folderName, xAxisLabels, linesArray, title):
	data = []
	for line in linesArray:
		line = list(line)
		lineName = line.pop(0)
		data.append(go.Scatter(
			x=xAxisLabels,
			y= line,
			mode = 'lines',
			name = lineName,
			line = dict(shape='line')
			))
	layout = go.Layout(
		title=title,
		yaxis = {
			'title': '%',
			'tickformat': ',.0%',
			'range': [0,1]
		}
		)
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

def create_groupTotal(folderName,total, x, title) : 
	trace = go.Bar(
		x=x,
		y=total,
		name='All devices'
	)
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
	fig = go.Figure(data=[trace], layout=layout)
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


def create_multiple_bars(folderName, dates, matrix, title, yaxisTitle = 'Number'):
	data = []
	for line in matrix.keys() :
		if line == 'Dates' :
			continue
		trace = go.Bar(
			x = dates,
			y = matrix[line],
			name= line
		)
		data.append(trace)
	yaxis = dict(title=yaxisTitle)
	if yaxisTitle == '%':
		yaxis['range']=[0,100]
	layout = go.Layout(
		title=title,
		yaxis = yaxis
	)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')	

def create_multiple_boxPlot(folderName, lines, title):
	data = []
	for line in lines:
		data.append(go.Box(x=lines[line], name=line, boxpoints = False))
	layout = go.Layout(
		title = title,
		xaxis=dict(title='Minutes', range=[0,35])
		)
	name = title.replace(' ','_')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename=folderName+'/'+name,sharing='private')			

def create_sankey(data):
	data_trace = dict(
		type='sankey',
	    domain = dict(
			x =  [0,1],
			y =  [0,1]
		),
		orientation = "h",
		valueformat = ".0f",
		node = dict(
			pad=15,
			thickness=15,
			line=dict(
				color="black",
				width=0.5
			),
			label =  data['node']['label'],
			color =  data['node']['color']
		),
		link=dict(
			source = data['link']['source'],
			target = data['link']['target'],
			value = data['link']['value'],
		)
	)
	layout = dict(
		title = 'Ceci est un graph test'
	)
	fig = go.Figure(data = [data_trace], layout = layout)
	py.plot(fig, filename='TEST/Sankey')


