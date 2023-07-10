import pandas as pd


class MainConvertor:
    def __init__(self):
        pass;

    def format_kg(self, df):
        nodes_df = df[['id', 'statement']]
        nodes_df['tag'] = "fake_news"
        max_value = df['id'].max()
        print(kg)

        unique_targets = kg[kg['edge'] == 'has_subject']['target'].unique()
        print(unique_targets)
        print("HEREEEE")
        initial_offset = len(unique_targets)
        target_nodes_df1 = pd.DataFrame({
            'id': [x + 1 + max_value for x in range(initial_offset)],
            'statement': unique_targets,
            'tag': ['topic'] * len(unique_targets)})
        nodes_df = pd.concat([nodes_df, target_nodes_df1])

        unique_targets = kg[kg['edge'] == 'contains_entity']['target'].unique()
        print(unique_targets)
        print("HEREEEE")
        second_offset = len(unique_targets) + initial_offset
        target_nodes_df2 = pd.DataFrame({
            'id': [x + 1 + max_value for x in range(initial_offset, second_offset)],
            'statement': unique_targets,
            'tag': ['entity'] * len(unique_targets)})
        nodes_df = pd.concat([nodes_df, target_nodes_df2])

        target_nodes_df = pd.concat([target_nodes_df1, target_nodes_df2])

        print(nodes_df.head())
        nodes_json = nodes_df.to_json(orient='records')

        target_ids = target_nodes_df['id'].values
        target_names = target_nodes_df['statement'].values
        encoded_kg = kg.replace(target_names, target_ids)
        print(encoded_kg.head())
        links_json = encoded_kg.to_json(orient='records')
        print(nodes_json)
        print(links_json)
        final_json = "{ \"nodes\":" + nodes_json + ", \"links\":" + links_json + "}"

        print(final_json)
        with open("datasets/kg/kg.json", "w") as outfile:
            outfile.write(final_json)
        print(final_json)

    def extract_entities(self, df):
        for index, row in df.iterrows():
            statement = row['statement']
            text_ents = row['entities']
            new_df = pd.DataFrame({'source': [row['id']] * len(text_ents),
                                   'target': text_ents,
                                   'edge': ['contains_entity'] * len(text_ents)})
            return new_df
    def convert_csv(self, filename):
        df = pd.read_csv(filename)
        kg = self.extract_entities(df)
        self.format_kg(kg)
