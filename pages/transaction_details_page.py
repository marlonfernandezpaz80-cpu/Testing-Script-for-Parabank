from playwright.sync_api import Page, expect

class TransactionDetailsPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Transaction Details")
        self.table = self.right_panel.locator("table")
        self.line = self.table.locator("tr")

    def is_loaded(self):
        expect(self.title).to_be_visible()

    def get_dats_dict(self):
        dats = []
        dats_dict = dict()
        for line in self.line.all_inner_texts():
            divided_line = line.split("\t")
            dats.append(divided_line[1])
        dats_dict["Transaction ID"] = dats[0]
        dats_dict["Date"] = dats[1]
        dats_dict["Description"] = dats[2]
        dats_dict["Type"] = dats[3]
        dats_dict["Amount"] = dats[4]
        return dats_dict

    def get_transaction_id(self):
        trans_dict = self.get_dats_dict()
        return trans_dict["Transaction ID"]

    def get_transaction_date(self):
        trans_dict = self.get_dats_dict()
        return trans_dict["Date"]

    def get_transaction_description(self):
        trans_dict = self.get_dats_dict()
        return trans_dict["Description"]
    
    def get_transaction_type(self):
        trans_dict = self.get_dats_dict()
        return trans_dict["Type"]

    def get_transaction_amount(self):
        trans_dict = self.get_dats_dict()
        return trans_dict["Amount"]

    def verificate_dats(self, id, date, description, type, amount):
        visible_id = self.get_transaction_id()
        assert visible_id == id
        visible_date = self.get_transaction_date()
        assert visible_date == date
        visible_description = self.get_transaction_description()
        assert visible_description == description
        visible_type = self.get_transaction_type()
        assert visible_type == type
        visible_amount = self.get_transaction_amount()
        assert visible_amount == amount
