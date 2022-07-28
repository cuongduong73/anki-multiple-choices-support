from ast import Try
from re import TEMPLATE
from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, askUser, showInfo
from anki.hooks import addHook
import random
from . import styles, version


DEFAULT_MODEL_NAME = "Multiple Choice (optional reversed card)"
CARD_1_NAME = "Card 1"
CARD_2_NAME = "Card 2"

TEMPLATE_ONE_SIDE = "One Side Note Type"
TEMPLATE_TWO_SIDE = "Two Sides Note Type"

class MultipleChoice(QDialog):
    """Main Options dialog"""

    def __init__(self, browser, nids) -> None:
        QDialog.__init__(self, parent=browser)
        self.browser = browser
        self.nids = nids
        self._setup_ui()


    def _setup_ui(self):
        """Set up widgets and layouts"""
        fields = self._get_fields()

        reversed_cb_label = QLabel("Add reversed?")
        self.reversed_cb = QCheckBox()
        self.reversed_cb.stateChanged.connect(self._on_changereversed)
        question_label = QLabel("Question Field")
        self.question_selection = QComboBox()
        self.question_selection.addItems(fields)
        answer_label = QLabel("Answer Field")
        self.answer_selection = QComboBox()
        self.answer_selection.addItems(fields)
        choice_label = QLabel("Choices Field")
        self.choice_selection = QComboBox()
        self.choice_selection.addItems(fields)
        r_choice_label = QLabel("Reversed Choices")
        self.r_choice_selection = QComboBox()
        self.r_choice_selection.addItems(fields)
        n_question_label = QLabel("#Choices")
        self.n_choice = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        row_idx = 1
        grid.addWidget(reversed_cb_label, row_idx, 0, 1, 1)
        grid.addWidget(self.reversed_cb, row_idx, 1, 1, 2)
        row_idx += 1
        grid.addWidget(question_label, row_idx, 0, 1, 1)
        grid.addWidget(self.question_selection, row_idx, 1, 1, 2)
        row_idx += 1
        grid.addWidget(answer_label, row_idx, 0, 1, 1)
        grid.addWidget(self.answer_selection, row_idx, 1, 1, 2)
        row_idx += 1
        grid.addWidget(choice_label, row_idx, 0, 1, 1)
        grid.addWidget(self.choice_selection, row_idx, 1, 1, 2)
        row_idx += 1
        grid.addWidget(r_choice_label, row_idx, 0, 1, 1)
        grid.addWidget(self.r_choice_selection, row_idx, 1, 1, 2)
        row_idx += 1
        grid.addWidget(n_question_label, row_idx, 0, 1, 1)
        grid.addWidget(self.n_choice, row_idx, 1, 1, 2)

        self.label_results = QLabel()
        self.label_results.setText("Ready!")
        self.preset_selection = QComboBox()
        self.template_selection = QComboBox()
        self.template_selection.addItems([TEMPLATE_ONE_SIDE, TEMPLATE_TWO_SIDE])
        update_notetype_btn = QPushButton("Update")
        update_notetype_btn.clicked.connect(self._on_update_notetype)


        info = QWidget()
        l_info = QVBoxLayout()
        l_info.addLayout(grid)
        info.setLayout(l_info)
        
        config_names = get_config_names()
        self.preset_selection.setEditable(True)
        self.preset_selection.currentIndexChanged.connect(self._on_changepreset)
        # self.preset_selection.addItem("Default")
        if len(config_names) > 0:
            self.preset_selection.addItems(config_names)

        dlt_btn = QPushButton("Delete")
        dlt_btn.clicked.connect(self._on_delete)    
        dlt_btn.setGeometry(20, 20, 20, 20)

        status_grid = QGridLayout()
        status_grid.setSpacing(10)
        row_idx = 1
        status_grid.addWidget(self.preset_selection, row_idx, 0, 1, 3)
        status_grid.addWidget(dlt_btn, row_idx, 3, 1, 1)
        row_idx += 1
        status_grid.addWidget(self.template_selection, row_idx, 0, 1, 3)
        status_grid.addWidget(update_notetype_btn, row_idx, 3, 1, 1)
        row_idx += 1
        status_grid.addWidget(self.label_results, row_idx, 0, 1, 4)
        status_bar = QWidget()
        l_status_bar = QVBoxLayout()
        l_status_bar.addLayout(status_grid)
        status_bar.setLayout(l_status_bar)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self._on_accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self._on_reject)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._on_save)
       
        btn_box = QDialogButtonBox()
        btn_box.addButton(add_btn, QDialogButtonBox.YesRole)
        btn_box.addButton(cancel_btn, QDialogButtonBox.RejectRole)
        btn_box.addButton(save_btn, QDialogButtonBox.AcceptRole)

        # Main layout
        l_main = QVBoxLayout()
        l_main.addWidget(info)
        l_main.addWidget(status_bar)
        l_main.addWidget(btn_box)
        self.setLayout(l_main)
        self.setMinimumWidth(360)       
        self.setWindowTitle('Multiple Choice Support - v{}'.format(version.__version__))
        self._on_changereversed(self.reversed_cb.isChecked())

    def _get_fields(self):
        nid = self.nids[0]
        mw = self.browser.mw
        model = mw.col.getNote(nid).model()
        fields = mw.col.models.fieldNames(model)
        return fields

    def _get_answer(self, ans_field):
        l_ans = []
        mw = self.browser.mw
        for nid in self.nids:
            note = mw.col.getNote(nid)
            ans = note[ans_field]
            if ans not in l_ans:
                l_ans.append(ans)
        return l_ans

    def _create_questions(self):
        fld_ans = self.answer_selection.currentText()
        fld_choice = self.choice_selection.currentText()
        fld_ques = self.question_selection.currentText()
        fld_r_choice = self.r_choice_selection.currentText()  
        nids = len(self.nids)
        
        is_reversed = self.reversed_cb.isChecked()
        l_ques = self._get_answer(fld_ques)
        l_ans = self._get_answer(fld_ans)
        n_ques_txt = self.n_choice.text()
        
        n_ques = 0
        if not n_ques_txt.isdigit():
            self.label_results.setText("ERROR! #Question isn't a number")
            return
        else: 
            n_ques = int(n_ques_txt)

        # on_confirm
        q = ("The contents of the field '{0}' and '{1}' will be replaced in {2} selected note(s).<br><br>Is this okay?").format(fld_choice, fld_r_choice, nids)
        if not askUser(q, parent=self):
            return

        mw = self.browser.mw
        mw.progress.start()
        self.browser.model.beginReset()

        cnt = 0
        for nid in self.nids:
            note = mw.col.getNote(nid)
            note = create_question_from_note(note, fld_ans, fld_choice, l_ans, n_ques)
            if is_reversed:
                note = create_question_from_note(note, fld_ques, fld_r_choice, l_ques, n_ques)
            else:
                note[fld_r_choice] = ""
            cnt += 1
            self.label_results.setText(("Processed  {0}/{1}").format(cnt, nids))
            mw.app.processEvents()
            note.flush()
        
        self.browser.model.endReset()
        mw.requireReset()
        mw.progress.finish()
        mw.reset()
        
        tooltip("Processed {0} notes.".format(cnt), parent=self.browser) 

    def _on_accept(self):
        self._create_questions()
        #self.close()
    
    def _on_reject(self):
        self.close()

    def _on_save(self):
        config_name = self.preset_selection.currentText()
        if config_name == "Default":
            self.label_results.setText("Can't overwrite \"Default\"!")
            return
        q = ("Do you really want to save current configuration to \"{0}\" preset?").format(config_name)
        if not askUser(q, parent=self):
            return        
        
        nid = self.nids[0]
        mw = self.browser.mw
        model = mw.col.getNote(nid).model()
        notetype = model["name"]
        
        cfg = mw.addonManager.getConfig(__name__)
        settings = cfg["settings"]
        
        configs = {}
        configs["reversed"] = self.reversed_cb.isChecked()
        configs["question_fld"] = self.question_selection.currentText()
        configs["answer_fld"] = self.answer_selection.currentText()
        configs["choice_fld"] = self.choice_selection.currentText()
        configs["r_choice_fld"] = self.r_choice_selection.currentText()
        configs["n_choice"] = self.n_choice.text()
        
        setting = {}
        setting["name"] = config_name
        setting["notetype"] = notetype
        setting["configs"] = configs

        is_existed = False
        
        for s in settings:
            if s["name"] == setting["name"]:
                s["notetype"] = setting["notetype"]
                s["configs"] = setting["configs"]
                cfg["settings"] = settings
                mw.addonManager.writeConfig(__name__, cfg)
                self.label_results.setText("Updated configuration!")
                is_existed = True
                break
        if not is_existed:
            settings.append(setting)
            cfg["settings"] = settings
            mw.addonManager.writeConfig(__name__, cfg)
            self.preset_selection.addItem(setting["name"])
            self.label_results.setText("Added configuration!")

    def _on_changereversed(self, idx):
        if idx:
            self.question_selection.setEnabled(True)
            self.r_choice_selection.setEnabled(True)
        else:
            self.question_selection.setEnabled(False)
            self.r_choice_selection.setEnabled(False)
    
    def _on_changepreset(self, idx):
        preset_name = self.preset_selection.itemText(idx)
        
        configs = get_config_by_name(preset_name)
        if configs:
            self.reversed_cb.setChecked(configs["reversed"])
            self.n_choice.setText(str(configs["n_choice"]))

            # find the index of the field in configuration
            idx_ques = self.question_selection.findText(configs["question_fld"])
            idx_ans = self.answer_selection.findText(configs["answer_fld"])
            idx_choice = self.choice_selection.findText(configs["choice_fld"])
            idx_r_choice = self.r_choice_selection.findText(configs["r_choice_fld"])
            
            # if not found the field name in configuration (idx = -1), set default idx to 0
            if idx_ques < 0:
                idx_ques = 0
            if idx_ans < 0:
                idx_ans = 0
            if idx_choice < 0:
                idx_choice = 0
            if idx_r_choice < 0:
                idx_r_choice = 0

            self.question_selection.setCurrentIndex(idx_ques)
            self.answer_selection.setCurrentIndex(idx_ans)
            self.choice_selection.setCurrentIndex(idx_choice)
            self.r_choice_selection.setCurrentIndex(idx_r_choice)

    def _on_delete(self):
        current_preset = self.preset_selection.currentText()
        if current_preset == "Default": 
            self.label_results.setText("Can't delete \"Default\"!")
            return
        q = ("Do you really want to delete current configuration to \"{0}\" preset?").format(current_preset)
        if not askUser(q, parent=self):
            return

        mw = self.browser.mw
        cfg = mw.addonManager.getConfig(__name__)
        settings = cfg["settings"]
        is_existed = False
        for setting in settings:
            if setting["name"] == current_preset:
                settings.remove(setting)
                self.preset_selection.removeItem(self.preset_selection.findText(current_preset))
                cfg["settings"] = settings
                mw.addonManager.writeConfig(__name__, cfg)
                self.label_results.setText("Delete preset \"{0}\"!".format(current_preset))
                self.preset_selection.setCurrentIndex(0)
                is_existed = True
                break
        if not is_existed:
            self.label_results.setText("Preset \"{0}\" not exist".format(current_preset))

    def _on_update_notetype(self):
        q = ("Be careful! This action will overwrite the \"{0}\" notetype. Please make sure you backed it up! <br><br>Are you sure?").format(DEFAULT_MODEL_NAME)
        if not askUser(q, parent=self):
            return
        try:
            update_template_model(DEFAULT_MODEL_NAME, self.template_selection.currentText())
        except Exception as e:
            info = ("Something's wrong! You should delete \"{0}\" notetype manually and try again! <br><br>Exception code: {1}").format(DEFAULT_MODEL_NAME, e)
            showInfo(info)
            self.label_results.setText("Update notetype failed!")
        else:
            # info = ("Update '{}' notetype success!").format(DEFAULT_MODEL_NAME)
            # showInfo(info)
            self.label_results.setText("Update notetype successful!")
        
def get_config_by_name(config_name):
    configs = {}
    cfg = mw.addonManager.getConfig(__name__)
    settings = cfg["settings"]

    for setting in settings:
        if setting["name"] == config_name:
            configs = setting["configs"]

    return configs

def get_config_names():
    names = []
    cfg = mw.addonManager.getConfig(__name__)
    settings = cfg["settings"]

    for setting in settings:
        names.append(setting["name"])
    return names

def update_template_model(model_name, ntype=TEMPLATE_ONE_SIDE):
    model = mw.col.models.by_name(model_name)
    model['css'] = styles.css.strip()

    if ntype == TEMPLATE_ONE_SIDE:
        for template in model["tmpls"]:
            if template["name"] == CARD_1_NAME:
                template['qfmt'] = styles.card1_front_template_one_side.strip()
                template['afmt'] = styles.card1_back_template_one_side.strip()
            if template["name"] == CARD_2_NAME:
                template['qfmt'] = styles.card2_front_template_one_side.strip()
                template['afmt'] = styles.card2_back_template_one_side.strip()
    elif ntype == TEMPLATE_TWO_SIDE:
        for template in model["tmpls"]:
            if template["name"] == CARD_1_NAME:
                template['qfmt'] = styles.card1_front_template_two_sides.strip()
                template['afmt'] = styles.card1_back_template_two_sides.strip()
            if template["name"] == CARD_2_NAME:
                template['qfmt'] = styles.card2_front_template_two_sides.strip()
                template['afmt'] = styles.card2_back_template_two_sides.strip() 
    else:
        raise Exception("{} invalid !!!".format(ntype))
    mw.col.models.update_dict(model)    


def create_new_model(model_name):
    model = mw.col.models.new(model_name)
    model['css'] = styles.css.strip()
    mw.col.models.addField(model, mw.col.models.newField("Id"))
    mw.col.models.addField(model, mw.col.models.newField("Question"))
    mw.col.models.addField(model, mw.col.models.newField("Answer"))
    mw.col.models.addField(model, mw.col.models.newField("Explanation"))
    mw.col.models.addField(model, mw.col.models.newField("Extra"))
    mw.col.models.addField(model, mw.col.models.newField("Choices"))
    mw.col.models.addField(model, mw.col.models.newField("Reversed Choices"))
    t1 = mw.col.models.newTemplate(CARD_1_NAME)
    t1['qfmt'] = styles.card1_front_template_one_side.strip()
    t1['afmt'] = styles.card1_back_template_one_side.strip()
    t2 = mw.col.models.newTemplate(CARD_2_NAME)
    t2['qfmt'] = styles.card2_front_template_one_side.strip()
    t2['afmt'] = styles.card2_back_template_one_side.strip()
    mw.col.models.addTemplate(model, t1)
    mw.col.models.addTemplate(model, t2)
    mw.col.models.add(model)

def display_dialog(browser):
    model_name = DEFAULT_MODEL_NAME
    if not mw.col.models.byName(model_name):
        mw.progress.start()
        browser.model.beginReset()
        create_new_model(model_name)
        browser.model.endReset()
        mw.requireReset()
        mw.progress.finish()
        mw.reset()

    nids = browser.selectedNotes()
    if not nids:
        tooltip("No cards selected.")
        return
    dialog = MultipleChoice(browser, nids)
    dialog.exec_()

def create_question(ans, l_ans, n_ques):
    n = 0
    output = ""
    l_ques = []
    
    n_ans = len(l_ans)
    n_count = 0
    if n_ans < n_ques:
        n_count = n_ans - 1
    else:
        n_count = n_ques

    loop_count = 0
    while n < n_count and loop_count < n_ans:
        loop_count += 1
        ques = random.choice(l_ans)
        if (ques != ans) and (ques not in l_ques):
            l_ques.append(ques)
            n += 1
    output = "|".join(l_ques)

    return output

def create_question_from_note(note, fld1, fld2, l_ans, n_ques):
    if (fld1 in note) and (fld2 in note):
        if note[fld1] != "":
            note[fld2] = create_question(note[fld1], l_ans, n_ques)
    return note

def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Multiple Choice Support')
    a.triggered.connect(lambda _, b=browser: display_dialog(b))

addHook("browser.setupMenus", setupMenu)

        
