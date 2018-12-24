#include "widget.h"
#include "ui_widget.h"
#include<QKeyEvent>
#include <QPushButton>
#include<QTextCodec>
#include <QFile>
#include <QMessageBox>
#include <QTextStream>
#include"qpainter.h"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
    ui->textEdit->setFocusPolicy(Qt::StrongFocus);
    ui->textBrowser->setFocusPolicy(Qt::NoFocus);

    ui->textEdit->setFocus();
    ui->textEdit->installEventFilter(this);//设置完后自动调用其eventFilter函数



}

Widget::~Widget()
{
    delete ui;
}
bool Widget::eventFilter(QObject *target, QEvent *event)
{
    if(target == ui->textEdit)
    {
        if(event->type() == QEvent::KeyPress)//回车键    on_pushButton_clicked  KeyPress
        {
             QKeyEvent *k = static_cast<QKeyEvent *>(event);
             if(k->key() == Qt::Key_Return)
             {
                 on_send_clicked();//开始“发送进程”
                 return true;
             }

        }
    }
    return QWidget::eventFilter(target,event);
}

void Widget::on_send_clicked()
{
    QString msg = ui->textEdit->toHtml(); //从edit到browser的过程

    QFile file("C:/Qt/test2/test24/test2.txt");//文件命名
    if (!file.open(QFile::WriteOnly | QFile::Text))     //检测文件是否打开
    {
        QMessageBox::information(this, "Error Message", "Please Select a Text File!");
        return;
    }
    QTextStream out(&file);                 //分行写入文件
    out << ui->textEdit->toPlainText();

    ui->textEdit->clear();
    ui->textEdit->setFocus();
    ui->textBrowser->append("user2:");
    ui->textBrowser->append(msg);


}




void Widget::on_pushButton_2_clicked()
{
    emit quit();
}



void Widget::on_pushButton_clicked()
{
    //将文本框数据取出并按行排列
        QFile file("C:/Qt/test2/test24/test2.txt");//文件命名
        if (!file.open(QFile::WriteOnly | QFile::Text))     //检测文件是否打开
        {
            QMessageBox::information(this, "Error Message", "Please Select a Text File!");
            return;
        }
        QTextStream out(&file);                 //分行写入文件
        out << ui->textEdit->toPlainText();

        QString msg = ui->textEdit->toHtml();//以下代码为从edit到browser的过程
        ui->textEdit->clear();//清屏
        ui->textEdit->setFocus();//将键盘焦点设置为指定窗口，窗口必须附加到调用线程的消息队列中
        ui->textBrowser->append("user2:");//打印
        ui->textBrowser->append(msg);//打印


}


void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.setBrush(Qt::white);
    painter.drawRect(this->rect());
}


void Widget::on_pushButton_3_clicked() //按钮三为打开本地文件
{
    QTextCodec*codec=QTextCodec::codecForName("GBK");//指定文本编码类型为“GBK”

    QFile file("C:/Qt/test2/test24/test2.txt");

    if(!file.open(QIODevice::ReadOnly|QIODevice::Text))//若打开失败直接返回
        return;

    while(!file.atEnd())//文件没到头
    {
        QByteArray line = file.readLine();//读取一行文本数据

        QString str = codec->toUnicode(line);//将读取到的行数据转换为Unicode格式
        ui->textBrowser->append("user 1:");
        ui->textBrowser->append(str);
    }
}
