import pandas as pd
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel(r'/Users/firatsoydinc/Desktop/Miuul/Week - 5/Ders Oncesi Notlar/ab_testing.xlsx',sheet_name= 'Control Group')
df_test  = pd.read_excel(r'/Users/firatsoydinc/Desktop/Miuul/Week - 5/Ders Oncesi Notlar/ab_testing.xlsx',sheet_name= 'Test Group')

#Data Cleaning
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

df_control['churn_rate'] = df_control['Impression']/df_control['Click']
df_test['churn_rate']= df_test['Impression']/ df_test['Click']

replace_with_thresholds(df_control,'churn_rate')
replace_with_thresholds(df_test,'churn_rate')


## Gorev - 1

# Varsayim Kontrolleri
#   - 1. Normallik Varsayımı
# H1: Degiskenler Normal Dagiliyor
# H0: Normal dagilmiyor
#################################################################
# Tum datanin Normalizasyon varsayimi
for each in df_control.columns:
    test_stat, pvalue = shapiro(df_control[each])
    print('Test Stat of ', each ,'= %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat of  Impression = 0.9697, p-value = 0.3514
#Test Stat of  Click = 0.9844, p-value = 0.8461
#Test Stat of  Purchase = 0.9773, p-value = 0.5891
#Test Stat of  Earning = 0.9756, p-value = 0.5306
#Test Stat of  churn_rate = 0.9548, p-value = 0.1107

for each in df_test.columns:
    test_stat, pvalue = shapiro(df_test[each])
    print('Test Stat of ', each ,'= %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat of  Impression = 0.9720, p-value = 0.4148
#Test Stat of  Click = 0.9896, p-value = 0.9699
#Test Stat of  Purchase = 0.9589, p-value = 0.1541
#Test Stat of  Earning = 0.9780, p-value = 0.6163
#Test Stat of  churn_rate = 0.9161, p-value = 0.0058

# Control veri setindeki tum veriler normal dagilim varsayimini saglarken
# Test veri setindeki churn rate verisi disindaki tum veriler normal dagilmaktadir.

# 2: Varyans Homojenligi
# H1: Degiskenlerin Varyanslari Homojen Dagiliyor
# H0: Homojen dagilmiyor
## Tum datanin varyans homojenligi kontrolu

for each1 in df_control.columns:
    test_stat, pvalue = levene(df_control[each1],df_test[each1])
    print('Test Stat of ', each1 ,'= %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat of  Impression = 0.5865, p-value = 0.4461
#Test Stat of  Click = 6.3041, p-value = 0.0141
#Test Stat of  Purchase = 2.6393, p-value = 0.1083
#Test Stat of  Earning = 0.3532, p-value = 0.5540
#Test Stat of  churn_rate = 0.7336, p-value = 0.3943

# Varsayim kontrolleri sonrasinda tum verinin varyans homojenligi varsayimini sagladigi gorulmektedir.
# Fakat churn rate normallik varsayimini saglamadigindan o degisken icin non-parametrik test yapilmalidir.


# Parametrik testlerin yapilmasi
# H1: Veriler arasinda anlamli bir fark vardir
# H0: Veriler arasinda anlamli bir fark yoktur

for each in df_control.columns:
    test_stat, pvalue = ttest_ind(df_control[each],
                               df_test[each],
                                  equal_var=True)
    print('Test Stat of ', each ,'= %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat of  Impression = -4.2966, p-value = 0.0000
#Test Stat of  Click = 4.4266, p-value = 0.0000
#Test Stat of  Purchase = -0.9416, p-value = 0.3493
#Test Stat of  Earning = -9.2545, p-value = 0.0000


#non-parametrik Test
# H1: Veriler arasinda anlamli bir fark vardir
# H0: Veriler arasinda anlamli bir fark yoktur

test_stat, pvalue = mannwhitneyu(df_control['churn_rate'],
                               df_test['churn_rate'])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 292.0000, p-value = 0.0000

# p value 0.05 ten kucuk oldugu icin H0 reject edilir.

# Gorev 2 - 3 - 4

# Ciktida da gorulecegi uzere Churn rate degiskenleri arasinda anlamli bir fark bulunmamaktadir.
# Impression  Click ve Earning degiskenlerinde anlamli bir fark varken purchase degiskenin anlamli bir
# fark yoktur. Bu nedenle eldeki data ile yorum yapmak istenildiginde bombabomba.com yoneticilerinin max bidding
# ile reklam vermemeye devam etmesi gerekmektedir. Cunku ne churn rate te ne de purchase degiskeninde
# her hangi bir degisiklik meydana gelmeyecektir. Fakat daha fazla data toplandiginda verinin durumu yeniden
# incelenebilir. Veri de tarih degiskeni bulunmadigindan Verinin guncellik durumuna bakilarak guncel veri ile sample calismasi yapilip guncel durum kontrolu yapilabilir.


