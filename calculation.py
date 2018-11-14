import datetime as d
import numpy as np
from statistics import mean
from collections import defaultdict


class calculate:
    def __init__(self):
        self.result = 0

    def meantime(self, issueobject):
        ymd_create = []
        ymd_resdate = []
        delta_t = []
        for i in range(0, len(issueobject)):
            ymd_create.append(d.datetime(int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[1]), int(issueobject[i].raw[u'fields']
                                                                                                                                                                                                     [u'created'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[1])))
            ymd_resdate.append(d.datetime(int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[1]), int(issueobject[i].raw[u'fields']
                                                                                                                                                                                                                    [u'resolutiondate'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[1])))
            delta_t.append((ymd_resdate[i] - ymd_create[i]).days)

        self.result = np.mean(np.array(delta_t))
        return self.result

    def mediantime(self, issueobject):
        ymd_create = []
        ymd_resdate = []
        delta_t = []
        for i in range(0, len(issueobject)):
            ymd_create.append(d.datetime(int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[1]), int(issueobject[i].raw[u'fields']
                                                                                                                                                                                                     [u'created'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[1])))
            ymd_resdate.append(d.datetime(int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[1]), int(issueobject[i].raw[u'fields']
                                                                                                                                                                                                                    [u'resolutiondate'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[1])))
            delta_t.append((ymd_resdate[i] - ymd_create[i]).days)

        self.result = np.median(np.array(delta_t))
        return self.result

    def variancetime(self, issueobject):
        ymd_create = []
        ymd_resdate = []
        delta_t = []
        for i in range(0, len(issueobject)):
            ymd_create.append(d.datetime(int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[1]), int(issueobject[i].raw[u'fields']
                                                                                                                                                                                                     [u'created'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[1])))
            ymd_resdate.append(d.datetime(int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[1]), int(issueobject[i].raw[u'fields']
                                                                                                                                                                                                                    [u'resolutiondate'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[1])))
            delta_t.append((ymd_resdate[i] - ymd_create[i]).days)

        self.result = np.var(np.array(delta_t))
        return self.result

    def personalinsight(self, issueobject):
        ymd_create = []
        ymd_resdate = []
        delta_t = []
        clist = []
        for i in range(0, len(issueobject)):
            ymd_create.append(d.datetime(int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[1]), int(
                issueobject[i].raw[u'fields'][u'created'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'created'].split('T')[1].split(':')[1])))
            ymd_resdate.append(d.datetime(int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[0].split('-')[1]), int(issueobject[i].raw[u'fields']
                                                                                                                                                                                                                    [u'resolutiondate'].split('T')[0].split('-')[2]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[0]), int(issueobject[i].raw[u'fields'][u'resolutiondate'].split('T')[1].split(':')[1])))
            delta_t.append((ymd_resdate[i] - ymd_create[i]).days)
            if issueobject[i].raw[u'fields'][u'assignee'] != None:
                clist.append([issueobject[i].raw[u'fields']
                              [u'assignee'][u'name'], delta_t[i]])
            else:
                pass
        dl = defaultdict(list)
        for k, v in clist:
            dl[k].append(v)
            means = [(k, mean(v)) for k, v in dl.items()]
        self.result = means
        return self.result
