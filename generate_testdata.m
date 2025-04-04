% -------------------------------------------------------------------------
% Load raw data and generate cleaned data used for analysis
% -------------------------------------------------------------------------

% Load data
clear; clc;
% for octave
% pkg load io;
  mc=1;
  [mdata,mtxt] = xlsread('testdata.xlsx');
  vartype      = 5*ones(1,93)
  names        = mtxt(1,2:end);
  [yt,a,b,c]   = prepare(mdata,names,vartype)
  data         = yt(3:end,:)
  T            = length(yt);
  dates        = 2000+(0:1/12:19-1/12)';
  dates        = dates(end-T+1:end);
  save testdata data dates names vartype

