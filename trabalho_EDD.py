# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

df_rides = pd.read_csv('df_rides.csv', sep=',')
df_stations = pd.read_csv('df_stations.csv', sep=',')

# transformando a coluna user_birthdate no tipo data
df_rides['user_birthdate'] = df_rides['user_birthdate'].astype("datetime64")

class ride:
    def __init__(self, gender, birthdate, residence, station_start):
        
        self.db = df_rides
        self.db_stations = df_stations
        
        gender_array = ['M','F']
        uf_array = ['AP', 'DF', 'SP', 'RS', 'PR', 'RJ', 'GO', 'AC', 'MA', 'PA', 'MG',
                    'RN', 'PE', 'MT', 'ES', 'PB', 'RR', 'BA', 'AL', 'PI', 'CE', 'SC',
                    'RO', 'AM', 'MS', 'TO', 'SE'] 
        
        status = True
        
        if gender in gender_array:
            pass
        else:
            status = False
            print("Não Possui essa informação de genero na base da dados")
            
        if  station_start in self.db_stations.station.unique():
            pass
        else:
            print("Não Possui essa informação de estação na base da dados")
            status = False    
            
        if  residence in uf_array:
            pass
        else:
            print("Não Possui essa informação de UF brasileiro na base da dados")
            status = False 
        
        if status:
            self.status = "Iniciado"
            self.gender = gender
            self.birthdate = birthdate
            self.residence = residence
            self.ride_date =  pd.Timestamp.now().strftime('%Y-%m-%d')
            self.time_start = pd.Timestamp.now().strftime('%H:%M:%S')
            self.station_start = station_start
            
            
            self.index = len(self.db.index)
            
            
            self.time_end = None
            self.station_end = None
            self.ride_duration = None
            self.ride_late = None
            
            insert_list = [self.gender,
                          self.birthdate,
                          self.residence,
                          self.ride_date,
                          self.time_start,
                          self.time_end,
                          self.station_start,
                          self.station_end,
                          self.ride_duration,
                          self.ride_late]
            
            print(insert_list)
            self.db.loc[self.index] = insert_list
            
        else:
            print('Erro de Validação ou insert na base')
                
    
    def user_age(self):
        print(int(str((pd.Timestamp.now() - pd.to_datetime(self.birthdate, format='%Y-%m-%d') ) /365)[:2].strip()))
        
    def get(self):
        
        get_list = [self.gender,
                    self.birthdate,
                    self.residence,
                    self.ride_date,
                    self.time_start,
                    self.time_end,
                    self.station_start,
                    self.station_end,
                    self.ride_duration,
                    self.ride_late]
        
        print(get_list)
        
    def finish_ride(self, station_end):
        
        status =  True
        
        if  station_end in self.db_stations.station.unique():
            pass
        else:
            print("Não Possui essa informação como padrão na base da dados")
            status = False
        
        if status:
            
            self.status = "Concluido"
            self.time_end = pd.Timestamp.now().strftime('%H:%M:%S')
            self.station_end =  station_end
            self.ride_duration = pd.Timedelta(pd.Timestamp.now() - pd.to_datetime(self.ride_date + ' ' + self.time_end)) / pd.Timedelta('60s')
            
            if self.ride_duration >= 60:
                self.ride_late =   1
            else:
                self.ride_late =   0
            
            insert_list = [self.gender,
                          self.birthdate,
                          self.residence,
                          self.ride_date,
                          self.time_start,
                          self.time_end,
                          self.station_start,
                          self.station_end,
                          self.ride_duration,
                          self.ride_late]
            
            print(insert_list)
            self.db.loc[self.index] = insert_list
            
        else:
            print('Erro de Validação ou insert na base')
