# search/search_service.py
import difflib

class SearchService:

    def exact_search(self, contacts, query):
        """Exact/substring search"""
        query = query.lower()
        results = []

        for record in contacts.values():
            fields_to_search = self.collect_fields(record)
            combined = " ".join(fields_to_search)

            if query in combined:
                results.append(record)

        return results

    def fuzzy_search(self, contacts, query, limit=3):
        """Fuzzy search if exact match fails"""
        query = query.lower()
        scored = []

        for record in contacts.values():
            fields_to_search = self.collect_fields(record)
            combined = " ".join(fields_to_search)

            score = difflib.SequenceMatcher(None, query, combined).ratio()
            scored.append((score, record))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [record for score, record in scored if score >= 0.3][:limit]

    def collect_fields(self, record):
        """Collect name, phones, email, address, birthday as lowercase strings"""
        fields = []

        if getattr(record, "name", None):
            fields.append(record.name.value.lower())

        for phone in getattr(record, "phones", []):
            fields.append(phone.value.lower())

        email = getattr(record, "email", None)
        if email:
            fields.append(email.value.lower())

        address = getattr(record, "address", None)
        if address:
            fields.append(address.value.lower())

        birthday = getattr(record, "birthday", None)
        if birthday:
            fields.append(str(birthday.value).lower())

        return fields