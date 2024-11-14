# blog/views.py
# define the views for the blog app
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import Voter
from datetime import date
import plotly
import plotly.graph_objs as go
import numpy as np




# Create your views here.
class VoterListView(ListView):
    '''View to show a list of voters.'''
    template_name = 'voter_analytics/results.html'  # Update template path
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100  # show 50 voter records per page
    years = list(reversed(range(1900, 2025))  )
    scores = list(range(1, 5))  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = self.years  
        return context


    def get_queryset(self) -> QuerySet[Any]:
        '''Limit the results to a small number of records'''
        qs = super().get_queryset()

        # party filter
        party = self.request.GET.get('party')
        if party:
            # added because didn't trim data, so need to match.
            party += " "
            qs = qs.filter(party=party)

        # min dob filter
        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            qs = qs.filter(dob__gte=date(int(min_dob), 1, 1))

        # max dob filter
        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            qs = qs.filter(dob__lte=date(int(max_dob), 12, 31))

        # voter score filter
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            qs = qs.filter(voter_score=voter_score)

        # voting filter
        if self.request.GET.get('v20state') == 'true':
            qs = qs.filter(v20state=True)
        if self.request.GET.get('v21town') == 'true':
            qs = qs.filter(v21town=True)
        if self.request.GET.get('v21primary') == 'true':
            qs = qs.filter(v21primary=True)
        if self.request.GET.get('v22general') == 'true':
            qs = qs.filter(v22general=True)
        if self.request.GET.get('v23town') == 'true':
            qs = qs.filter(v23town=True)

        return qs


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    '''View to show graphs of aggregated voter data.'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'v'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        v = context['v']

        # Histogram of Voters by Year of Birth
        
    
        yearcount = {}
        partycount = {}
        electioncount = {}


        for x in v:
            if x.party in partycount:
                partycount[x.party] += 1
            else:
                partycount[x.party] = 1

            if x.dob.year in yearcount:
                yearcount[x.dob.year] += 1
            else:
                yearcount[x.dob.year] = 1
            for i in range (0,6):
                # print(str(x).split(',')[2][i])
                if str(x).split(',')[2][i]:
                    if i in electioncount:
                        electioncount[i] += 1
                    else:
                        electioncount[i] = 1
       
        # year bar graph

        x = list(yearcount.keys())
        y = list(yearcount.values())  


        fig = go.Bar(x=x, y=y)
        yeargraph = plotly.offline.plot({'data':[fig]},
                                      auto_open=False,
                                      output_type='div')
        context['yeargraph'] = yeargraph

        # party pie chart

        x = list(partycount.keys())
        y = list(partycount.values()) 

        fig = go.Pie(labels=x, values=y)
        partygraph = plotly.offline.plot({'data':[fig]},
                                      auto_open=False,
                                      output_type='div')
        
        context['partygraph'] = partygraph

        # election bar graph

        x = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        y = list(electioncount.values())  

        fig = go.Bar(x=x, y=y)
        electiongraph = plotly.offline.plot({'data':[fig]},
                                      auto_open=False,
                                      output_type='div')
        context['electiongraph'] = electiongraph



        # Histogram of Voter Participation in Elections
        
      
        # build a pie chart
        # x = ['first half time', 'second half time']
        # y = [g.first_half_seconds, g.second_half_seconds]
        # # print(f'x={x}')
        # # print(f'y={y}')
        # fig = go.Pie(labels=x, values=y)
        # pie_div = plotly.offline.plot({'data':[fig]},
        #                               auto_open=False,
        #                               output_type='div')
        
        # # add the pie chart to the context
        # context['pie_div'] = pie_div
        # # create a bar chart with the number of runners passed and who passed by
        # x = [f'runners passed by {r.first_name}',
        #      f'runner who passed {r.first_name}']
        # y = [r.get_runners_passed(),
        #      r.get_runners_passed_by()]
        # # print(f'x={x}')
        # # print(f'y={y}')
        # fig = go.Bar(x=x, y=y)
        # bar_div = plotly.offline.plot({'data':[fig]},
        #                               auto_open=False,
        #                               output_type='div')
        # # add this to the context data for use in the template
        # context['bar_div'] = bar_div

        return context
