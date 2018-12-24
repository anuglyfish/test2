#include "widget.h"
#include <QApplication>
#include <QPushButton>
#include <QFont>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Widget w;
    w.show();

    QPushButton label("Succeed in ");
    label.resize(100,100);
    label.setFont(QFont("Times",18,QFont::Bold));

    QObject::connect(&w,SIGNAL(quit()),&a,SLOT(quit()));

    QObject::connect(&label,SIGNAL(clicked()),&a,SLOT(label()));

    label.show();




    return a.exec();
}
