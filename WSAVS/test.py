#coding:utf-8

import Draw
import History
import Freq

a = raw_input('')
rank = Freq.freq_analysis(a)
Freq.freq_insert(rank,a)