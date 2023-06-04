out = dat_std.ix[:,1]*dat_std.ix[:,2]

all = range(4,41)
f=open('result.log','w')
f.write('First,Second,Third,Score\n')
for x in itertools.combinations(all,3):
    inp = dat_std.ix[:,list(x)]
    regressor = MLPRegressor(hidden_layer_sizes = 10, activation = 'logistic', solver = 'lbfgs')
    regressor.fit(inp,out)
    f.write(str(x[0])+','+str(x[1])+','+str(x[2])+','+str(regressor.score(inp,out))+'\n')
f.close()