import pandas as pd

data = pd.read_csv(r'./chlorophyll.csv')

max_weeks = 19

data = data.drop_duplicates()

data['grid'] = data['Latitude'].astype(str) +','+ data['Longitude'].astype(str)
cells = data.grid.unique()

weeks = [str(i)+'W' for i in range(max_weeks)]

for k in range(max_weeks):
    df = []
    shift = 7*k
    for cell in cells:
        print(k,cell)
        work = data[data['grid']==cell]
        n = len(work)
        agg = []
        for i in range(n):
            chlor = 0
            t = 0
            for j in range(7):
                if i-shift-j >=0:
                    if not pd.isnull(work.iloc[i-shift-j,3]):
                        chlor += work.iloc[i-shift-j,3]
                        t +=1
            if t != 0:
                chlor = chlor/t
                agg.append(chlor)
            else:
                agg.append('')
        work[weeks[k]] = agg

        df.append(work)

    all = pd.concat(df)

    if k !=0:
        dataset = pd.merge(dataset,all)
    else:
        dataset = all

dataset.to_csv(r'lag.csv',index = False)  