# Peut-on établir un lien entre la densité de médecins par spécialité et par territoire et la pratique du
# dépassement d'honoraires ? Est-ce  dans les territoires où la densité est la plus forte que les médecins
# pratiquent le moins les dépassement d'honoraires ? Est ce que la densité de certains médecins / praticiens est
# corrélé à la densité de population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers
# etc...) ?

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import mpld3

plt.style.use('ggplot')

url_data = 'http://www.data.drees.sante.gouv.fr/ReportFolders/reportFolders.aspx?IF_ActivePath=P,490,497,514'

data_spe = 'Effectif_et_densite_par_departement_en_2014.xls'
data_honoraires = 'Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'

data_population = 'DEPAPOEFPO39EFFELP642.csv'


def load_data(data_spe, data_honoraires):
    # Read CSV
    df_spe = pd.read_excel(data_spe, sheetname=['Spécialistes', 'Généralistes et MEP'], na_values="nc")
    df_honoraires = pd.read_excel(data_honoraires, sheetname=['Spécialistes', 'Généralistes et MEP'], na_values="nc")

    # Remove rows with empty values
    df_spe_spec = df_spe.get('Spécialistes')[
        ['Spécialistes', 'DEPARTEMENT', 'EFFECTIF', 'POPULATION FRANCAISE', 'DENSITE /100 000 hab.']].dropna(axis=0,
                                                                                                             how='any')
    df_spe_medge = df_spe.get('Généralistes et MEP')[
        ['Généralistes et compétences MEP', 'DEPARTEMENT', 'EFFECTIF', 'POPULATION FRANCAISE',
         'DENSITE /100 000 hab.']].dropna(axis=0, how='any')

    # Rename Specialistes and Generalistes
    df_spe_spec.rename(columns={'Spécialistes': 'Type'}, inplace=True)
    df_spe_medge.rename(columns={'Généralistes et compétences MEP': 'Type'}, inplace=True)
    df_spe_spec = df_spe_spec[df_spe_spec.Type.str.contains("TOTAL") == False]
    df_spe_spec = df_spe_spec[df_spe_spec.DEPARTEMENT.str.contains("TOTAL") == False]
    df_spe_medge = df_spe_medge[df_spe_medge.Type.str.contains("TOTAL") == False]
    df_spe_medge = df_spe_medge[df_spe_medge.DEPARTEMENT.str.contains("TOTAL") == False]

    df_honoraires_spec = df_honoraires.get('Spécialistes').dropna(axis=0, how='any')
    df_honoraires_medge = df_honoraires.get('Généralistes et MEP').dropna(axis=0, how='any')

    # Rename Specialistes and Generalistes
    df_honoraires_spec.rename(columns={'Spécialistes': 'Type'}, inplace=True)
    df_honoraires_medge.rename(columns={'Généralistes et compétences MEP': 'Type'}, inplace=True)
    df_honoraires_spec = df_honoraires_spec[df_honoraires_spec.Type.str.contains("TOTAL") == False]
    df_honoraires_spec = df_honoraires_spec[df_honoraires_spec.DEPARTEMENT.str.contains("TOTAL") == False]
    df_honoraires_medge = df_honoraires_medge[df_honoraires_medge.Type.str.contains("TOTAL") == False]
    df_honoraires_medge = df_honoraires_medge[df_honoraires_medge.DEPARTEMENT.str.contains("TOTAL") == False]

    return df_spe_spec, df_spe_medge, df_honoraires_spec, df_honoraires_medge


def load_population(csvfile):
    df = pd.read_csv(csvfile, skiprows=9, sep=';', header=0,
                     usecols=['Unnamed: 0', 'Pop. totale : 20-39 ans', 'Pop. totale : 60-74 ans',
                              'Pop. totale : 0-19 ans',
                              'Pop. totale : 40-59 ans', 'Pop. totale : 75 ans et +'])
    df = df.drop(axis=0, labels=0)
    print(df)


def index_spe(df_honoraires):
    num = df_honoraires['STypes']
    df = pd.DataFrame(num.drop_duplicates())

    df.loc[:, 'ind'] = num.str.split("- ").str.get(0)
    df.loc[:, 'Spécialistes'] = num.str.split("- ").str.get(1)
    mask = (df['ind'].str.len() < 3)
    df = df.loc[mask]
    df.loc[:, 'ind'] = df['ind'].astype(int)
    df = df.set_index('ind')
    df = df.sort_index()
    return df


def assign_index(df_spe):
    vals = pd.DataFrame(df_spe.columns.values[3:], columns=["Type"])
    vals['Type'] = vals['Type'].str.replace('?', 'é')

    # print(vals)
    return vals


def melt_df(df):
    melt = df.melt(id_vars=['Type', 'DEPARTEMENT'])

    return melt


def stack_spe(df):
    stacked = df.stack()
    return stacked


def plot_spe(stacked):
    for i in range(1, 10):
        print(stacked[i])
        data = stacked[i].drop('SPECIALITE', axis=0).astype(float)
        plt.scatter(np.arange(0, len(data)), data.values, label=i)
    plt.show()
    plt.close()


def plot_honoraire(df_honoraires):
    print(df_honoraires)

    mask = (df_honoraires['Type'].str.split("- ").str.get(0).str.len() < 3)
    df = df_honoraires.loc[mask]

    fig, ax = plt.subplots()

    ax.scatter(df['EFFECTIFS'], df['DEPASSEMENTS (Euros)'], marker='+',
               c=df['Type'].str.split("- ").str.get(0))

    for i in range(len(df)):
        ax.text(df['EFFECTIFS'].values[i], df['DEPASSEMENTS (Euros)'].values[i],
                df['Type'].values[i].split("- ")[0], fontsize=6)

    plt.xlabel('Effectifs')
    plt.ylabel('Dépassements')
    plt.show()
    plt.close()


def join_all_spe(df_spe, df_honoraires):
    all = pd.merge(df_spe, df_honoraires, on=['Type', 'DEPARTEMENT'])

    return all


def join_all_medge(df_spe, df_honoraires):
    all = pd.merge(df_spe, df_honoraires, on=['Type', 'DEPARTEMENT'])

    return all


def plot_data(all):
    mask = (all['Type'].str.split("- ").str.get(0).str.len() < 3)
    df = all.loc[mask]

    fig, ax = plt.subplots()
    ax.scatter(df['DENSITE /100 000 hab.'], df['TOTAL DES HONORAIRES (Euros)'], marker='+',
               c=df['Type'].str.split("- ").str.get(0))

    plt.show()
    plt.close()


def info_data(all):
    mask = (all['Type'].str.split("- ").str.get(0).str.len() < 3) & (all['Type'].str.contains('TOTAL') == False)
    df = all.loc[mask]

    sorted_df = df.sort_values(by='DEPASSEMENTS (Euros)', ascending=False)

    fig, ax = plt.subplots()

    cmap = plt.cm.viridis

    sorted_df.loc[:, 'Type_formatted'] = sorted_df['Type'].str.split("- ").str.get(0).astype(int)

    types_distinct = sorted_df['Type'].str.split("- ").str.get(1).drop_duplicates()
    colors = cmap(np.linspace(0, 3, len(types_distinct) + 1))

    type_indexed = {types_distinct.values[i]: i for i in
                    range(len(types_distinct.values))}

    dico_colors = {t: colors[t] for t in type_indexed.values()}

    # for i, dff in sorted.groupby('Type'):
    #     spe = i.split("- ")[1]
    #
    #     scatter = ax.scatter(dff['DENSITE /100 000 hab.'], dff['TOTAL DES HONORAIRES (Euros)'],
    #                c=dico_colors[type_indexed[spe]], label=spe, alpha=0.4)

    density = sorted_df['DENSITE /100 000 hab.'].values
    honoraires = sorted_df['TOTAL DES HONORAIRES (Euros)'].values
    col = [dico_colors[type_indexed[t.split('- ')[1]]] for t in sorted_df['Type'].values]
    scatter = ax.scatter(density, honoraires, c=col, alpha=0.4)

    plt.xlabel('DENSITE /100 000 hab.')
    plt.ylabel('DEPASSEMENTS (Euros)')

    labels = [sorted_df['Type'].values[i] for i in range(len(sorted_df))]

    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.save_html(fig, 'type_spe.html')

    plt.show()
    plt.close()


def info_data_legend(all):
    mask = (all['Type'].str.split("- ").str.get(0).str.len() < 3) & (all['Type'].str.contains('TOTAL') == False)
    df = all.loc[mask]

    sorted = df.sort_values(by='DEPASSEMENTS (Euros)', ascending=False)

    fig, ax = plt.subplots()

    cmap = plt.cm.viridis

    sorted.loc[:, 'Type_formatted'] = sorted['Type'].str.split("- ").str.get(0).astype(int)

    types_distinct = sorted['Type'].str.split("- ").str.get(1).drop_duplicates()
    colors = cmap(np.linspace(0, 3, len(types_distinct) + 1))

    type_indexed = {types_distinct.values[i]: i for i in
                    range(len(types_distinct.values))}

    dico_colors = {t: colors[t] for t in type_indexed.values()}

    for i, dff in sorted.groupby('Type'):
        spe = i.split("- ")[1]

        ax.scatter(dff['DENSITE /100 000 hab.'], dff['TOTAL DES HONORAIRES (Euros)'],
                   c=dico_colors[type_indexed[spe]], label=spe, alpha=0.4)

    plt.xlabel('DENSITE /100 000 hab.')
    plt.ylabel('DEPASSEMENTS (Euros)')

    handles, labels = ax.get_legend_handles_labels()

    interactive_legend = mpld3.plugins.InteractiveLegendPlugin(handles,
                                                               labels,
                                                               alpha_unsel=0.5,
                                                               alpha_over=1.5,
                                                               start_visible=False)

    mpld3.plugins.connect(fig, interactive_legend)
    mpld3.save_html(fig, 'type_spe_legend.html')


def apply_pca(df, size_spe):
    X = df[['DENSITE /100 000 hab.', 'DEPASSEMENTS (Euros)', 'TOTAL DES HONORAIRES (Euros)']].as_matrix()

    color = ['crimson'] * size_spe + ['mediumaquamarine'] * (len(df) - size_spe)

    scaler = StandardScaler().fit(X)
    X_std = scaler.transform(X)
    pca = PCA(n_components=2)
    pca.fit(X_std)

    print(pca.explained_variance_ratio_)

    print(pca.components_)

    X_transformed = pca.transform(X_std)
    plt.scatter(X_transformed[:, 0], X_transformed[:, 1], marker='+', alpha=0.6, c=color)

    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.show()
    plt.close()


if __name__ == "__main__":
    df_spe_spec, df_spe_medge, df_honoraires_spec, df_honoraires_medge = load_data(data_spe, data_honoraires)

    all_spe = join_all_spe(df_spe_spec, df_honoraires_spec)
    all_medge = join_all_medge(df_spe_medge, df_honoraires_medge)

    frames = [all_spe, all_medge]
    concatenation = pd.concat(frames)

    # if os.path.isfile('lol.csv'):
    # os.remove('lol.csv')
    # concatenation.to_csv('lol.csv', sep=';')

    info_data(concatenation)

    # apply_pca(concatenation, len(all_spe))

    # load_population(data_population)
