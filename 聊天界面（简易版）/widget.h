#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

#include<QTextStream>
#include<QFile>
#include<QIODevice>

namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();
    void paintEvent(QPaintEvent *);
protected:
    bool eventFilter(QObject *target, QEvent *event);//事件过滤器



private slots:
    void on_send_clicked();



    void on_pushButton_2_clicked();




    void on_pushButton_clicked();

    void on_pushButton_3_clicked();

signals:
    void quit();

private:
    Ui::Widget *ui;
};

#endif // WIDGET_H
