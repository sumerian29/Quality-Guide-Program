import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, 
                            QDialog, QTextEdit, QDialogButtonBox, QMessageBox)
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QTransform
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QDesktopServices

class QualityGuideApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("دليل الجودة - شركة نفط ذي قار")
        self.setGeometry(200, 100, 900, 600)

        # تشغيل الموسيقى الخلفية مع التكرار
        self.music_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.music_player.setAudioOutput(self.audio_output)
        self.music_player.setSource(QUrl.fromLocalFile("background_music.mp3"))
        self.audio_output.setVolume(0.5)
        self.music_player.mediaStatusChanged.connect(self.repeat_music)
        self.music_player.play()

        # إعداد الواجهة الرئيسية
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # تخصيص الألوان
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1E1E2E"))
        self.setPalette(palette)

        # تخطيط عام
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # شريط العنوان
        header_layout = QHBoxLayout()
        
        # شعار دوار
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("sold.png")
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_logo)
        self.timer.start(100)
        self.update_logo()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        header_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # عنوان الوزارة
        ministry_label = QLabel("وزارة النفط العراقية")
        ministry_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        ministry_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ministry_label.setStyleSheet("color: #ffffff; padding: 10px;")
        header_layout.addWidget(ministry_label)

        self.layout.addLayout(header_layout)

        # عنوان التطبيق
        title_label = QLabel("📜 دليل الجودة - شركة نفط ذي قار")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #ffffff; padding: 10px;")
        self.layout.addWidget(title_label)

        # نظام الصفحات
        self.pages = QStackedWidget()
        self.layout.addWidget(self.pages)

        # إنشاء الصفحات
        self.home_page = self.create_page(
            "🎉 مرحباً بك في دليل الجودة!", 
            "🔹 اضغط على الأزرار للتنقل بين الأقسام المختلفة.", 
            "#ff9800",
            add_pdf_buttons=True
        )
        self.policy_page = self.create_page("📜 سياسة الجودة", "✅ هذه هي سياسة الجودة الخاصة بالشركة.", "#007bff")
        self.goals_page = self.create_page("🎯 الأهداف", "📌 هذه هي الأهداف والمبادئ الأساسية للجودة.", "#28a745")

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.policy_page)
        self.pages.addWidget(self.goals_page)

        # إعداد التنقل
        self.create_navigation()

        # زر التدقيق الداخلي
        self.audit_button = QPushButton("📘 عرض دليل التدقيق الداخلي")
        self.audit_button.clicked.connect(self.show_audit_guide)
        self.layout.addWidget(self.audit_button)

        # تذييل الصفحة
        self.footer_label = QLabel("تصميم: ر. مهندسين أقدم طارق مجيد")
        self.footer_label.setFont(QFont("Arial", 10))
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.footer_label.setStyleSheet("color: #ffffff; padding: 10px;")
        self.layout.addWidget(self.footer_label)

    def rotate_logo(self):
        """تدوير الشعار بزاوية محددة"""
        self.angle += 2
        if self.angle >= 360:
            self.angle = 0
        self.update_logo()

    def update_logo(self):
        """تحديث صورة الشعار المدور"""
        transform = QTransform().rotate(self.angle, Qt.Axis.YAxis)
        rotated_pixmap = self.logo_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(rotated_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

    def create_page(self, title, description, color, add_pdf_buttons=False):
        """إنشاء صفحة جديدة مع خيارات PDF"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        # العنوان
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {color}; padding: 10px;")

        # الوصف
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 14))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #ffffff; margin-bottom: 20px;")

        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        # إضافة أزرار PDF إذا مطلوب
        if add_pdf_buttons:
            btn_procedures = QPushButton("📁 عرض إجراءات الجودة (PDF)")
            btn_procedures.clicked.connect(lambda: self.open_pdf("اسماء الاجراءات.pdf"))
            layout.addWidget(btn_procedures)

            btn_member = QPushButton("📁 مهام عضو الارتباط (PDF)")
            btn_member.clicked.connect(lambda: self.open_pdf("مهام عضو الارتباط.pdf"))
            layout.addWidget(btn_member)

            btn_system = QPushButton("📘 متطلبات نظام الجودة (PDF)")
            btn_system.clicked.connect(lambda: self.open_pdf("متطلبات نظام ادارة الجودة.pdf"))
            layout.addWidget(btn_system)

            btn_iso = QPushButton("📘 فوائد المواصفة ISO (PDF)")
            btn_iso.clicked.connect(lambda: self.open_pdf("فوائد المواصفة ISO9001.pdf"))
            layout.addWidget(btn_iso)

        return page

    def create_navigation(self):
        """إنشاء أزرار التنقل بين الصفحات"""
        home_btn = QPushButton("🏠 الرئيسية")
        policy_btn = QPushButton("📜 سياسة الجودة")
        goals_btn = QPushButton("🎯 الأهداف")

        # إضافة الأهداف التطويرية لصفحة الأهداف
        goals_pdf_btn = QPushButton("📁 الأهداف التطويرية 2025 (PDF)")
        goals_pdf_btn.clicked.connect(lambda: self.open_pdf("الاهداف التطويرية.pdf"))
        self.goals_page.layout().addWidget(goals_pdf_btn)

        # ربط الأزرار بالصفحات
        home_btn.clicked.connect(lambda: self.pages.setCurrentWidget(self.home_page))
        policy_btn.clicked.connect(lambda: self.pages.setCurrentWidget(self.policy_page))
        goals_btn.clicked.connect(lambda: self.pages.setCurrentWidget(self.goals_page))

        self.layout.addWidget(home_btn)
        self.layout.addWidget(policy_btn)
        self.layout.addWidget(goals_btn)

    def show_audit_guide(self):
        """عرض دليل التدقيق الداخلي"""
        dialog = QDialog(self)
        dialog.setWindowTitle("📘 دليل التدقيق الداخلي")
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setStyleSheet("background-color: white; border: 2px solid #004d00; border-radius: 12px;")
        dialog.setMinimumSize(800, 600)

        # منطقة النص
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setFont(QFont("Arial", 11))
        text_area.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_area.setStyleSheet("""
            background-color: #f4f4f4;
            color: #003300;
            padding: 15px;
            text-align: right;
        """)

        try:
            with open("التدقيق الداخلي البرنامج.txt", "r", encoding="utf-8") as file:
                content = file.read()
                html_content = f"""
                <html dir='rtl'>
                <head>
                <style>
                    body {{
                        font-family: 'Arial';
                        direction: rtl;
                        text-align: right;
                        padding: 20px;
                    }}
                    h1 {{
                        color: #004d00;
                        margin-bottom: 20px;
                    }}
                    p {{
                        margin-bottom: 12px;
                        line-height: 1.6;
                        text-align: justify;
                    }}
                </style>
                </head>
                <body>
                <h1>📘 دليل التدقيق الداخلي</h1>
                <p>{content.replace("\n", "</p><p>")}</p>
                </body>
                </html>
                """
                text_area.setHtml(html_content)
        except FileNotFoundError:
            text_area.setPlainText("تعذر العثور على ملف دليل التدقيق الداخلي.")

        # أزرار الإغلاق
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)

        # تخطيط النافذة
        layout = QVBoxLayout()
        layout.addWidget(text_area)
        layout.addWidget(buttons)
        dialog.setLayout(layout)

        dialog.exec()

    def open_pdf(self, filename):
        """فتح ملف PDF باستخدام التطبيق الافتراضي"""
        path = os.path.join(os.getcwd(), filename)
        if os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            QMessageBox.warning(self, "خطأ", f"الملف {filename} غير موجود!")

    def repeat_music(self, status):
        """إعادة تشغيل الموسيقى عند الانتهاء"""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.music_player.setPosition(0)
            self.music_player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QualityGuideApp()
    window.show()
    sys.exit(app.exec())