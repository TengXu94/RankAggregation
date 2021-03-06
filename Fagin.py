import ScorerFileManager


class Fagin:
    def __init__(self):
        self.sfm = ScorerFileManager.ScorerFileManager()
        self.dictionary_text_query = self.sfm.get_out_cran_eng_stop_text_bm25()  # Dictionary of DICTIONARIES
        self.dictionary_title_query = self.sfm.get_out_cran_eng_stop_title_bm25()  # Dictionary of DICTIONARIES

    def fagin_algorithm(self, query_id, k):

        if (str(query_id) not in self.dictionary_text_query or str(query_id) not in self.dictionary_title_query):   #TO CHANGE
            return None

        dictionary_title_doc = self.dictionary_title_query.get(str(query_id))  # Dictionary
        dictionary_text_doc = self.dictionary_text_query.get(str(query_id))  # Dictionary

        iterator_title_doc = iter(dictionary_title_doc.keys())  # Iterator on keys
        iterator_text_doc = iter(dictionary_text_doc.keys())  # Iterator on keys

        memory = {}
        results = []

        i = 0
        counter = k

        while (counter > 0 and i < 200):
            item_title = next(iterator_title_doc)
            item_text = next(iterator_text_doc)

            if item_title not in memory:
                memory[item_title] = 1
            else:
                memory[item_title] += 1

            if item_text not in memory:
                memory[item_text] = 1
            else:
                memory[item_text] += 1

            if memory[item_text] == 2:
                counter -= 1

            if memory[item_title] == 2:
                if item_text != item_title:
                    counter = - 1

            i += 1

        for value in memory:
            if value in dictionary_text_doc and value in dictionary_title_doc:
                results.append((value, 2 * float(dictionary_title_doc[value]) + float(dictionary_text_doc[value])))
            else:
                if value not in dictionary_text_doc:
                    results.append((value, 2 * float(dictionary_title_doc[value])))
                else:
                    results.append((value, float(dictionary_text_doc[value])))

        return sorted(results, key=lambda x: x[1], reverse=True)
