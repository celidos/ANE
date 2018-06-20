import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий

from PyQt5 import QtWidgets
from PyQt5.QtCore import qDebug


import design  # Это наш конвертированный файл дизайна
import site_handler_globus as GLOBUS
from price_manager import PriceManager

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btnBrowse.clicked.connect(self.browse_folder)  # Выполнить функцию browse_folder
                                                            # при нажатии кнопки

        self.listWidget.itemClicked.connect(self.update_shop_listing)
        self.listWidget_2.itemClicked.connect(self.update_price_listing)

        # self.tableView.setStyleSheet('::item { padding: 0px }')

        qDebug('gay attack!')

        # globus = GLOBUS.SiteHandlerGlobus()
        # globus.get_all_pricelists()

        self.manager = PriceManager()
        self.manager.load_handlers_to_table(self.listWidget)

        # --- insert init here ---

    def update_shop_listing(self, item):
        self.manager.load_available_product_prices_to_table(self.listWidget.currentRow(), self.listWidget_2)

    def update_price_listing(self, item):
        self.manager.load_price_for_product_to_table(self.listWidget.currentRow(),
                                                     self.listWidget_2.currentRow(),
                                                     self.tableView)

    def browse_folder(self):
        # self.listWidget.clear()  # На случай, если в списке уже есть элементы
        # directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # # открыть диалог выбора директории и установить значение переменной
        # # равной пути к выбранной директории
        #
        # if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
        #     for file_name in os.listdir(directory):  # для каждого файла в директории
        #         self.listWidget.addItem(file_name)   # добавить файл в listWidget
        self.manager.get_all_prices_from_all_sites()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
