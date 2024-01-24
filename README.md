# Expiration Check

#### 開發目的
- 為了解決家裡零食太多，導致記不起來每個零食的過期日期，所以設計一個Linebot紀錄新增的零食，並設置「緊急專區」，讓使用者一按下按鈕即可瞭解家裡有哪些食物會在7天內過期。
#### 使用指南
- 食物一覽表：顯示所有目前有的食物，以“1.(食物名稱)是在(新增時間）進來的，並會在(食物過期日)過期。” 顯示。
- 新增食物：點選此選項，Linebot會再問要新增的食物名稱及過期日期，並加入至資料庫。
- 刪除食物：點選此選項，Linebot會再問要刪除的食物名稱，並將此食物從資料庫中刪除。
- 需要緊急處理的食物：此選項會列出所有會在7天內過期的食物。
#### 開發技術
- Linebot
- Django
- Postgresql
- Render
> 網路上很多關於Linebot deploy在Heroku的文章，但因Heroku不再支援免費服務，故選擇Render

#### 在Render上部署
1. 先將專案推至Github上，成為一個repository
2. 在Render的主頁中先新增一個POSTGRESQL資料庫，並記起此資料庫的**Internel URL**
3. 建立好資料庫後，就去新增一個Web Services
4. 在Web Services的設定中，需要在環境變數(Environment Variables)加入Line channel access token、Line channel secrets和Database URL(就是新增資料庫的Internel URL)
5. Start command 為 pip install -r requirements.txt
6. Build command 為 gunicorn (linebot名稱).wsgi:application
> linebot名稱就看你的setting放在哪個資料夾，此資料夾名稱就是linebot名稱
7. 接著就可以deploy push在Github上面的專案了！
> 每push一次，系統就會自動重新deploy新的commit

#### 額外新增的檔案
1. requirements.txt
2. build.sh

#### 參考資料 - Render
[How to Deploy a Django App on Render](https://www.freecodecamp.org/news/deploying-a-django-app-to-render/)

[Deploy Your Django App with Ease: A Step-by-Step Guide with Render](https://medium.com/django-unleashed/deploy-your-django-app-with-ease-a-step-by-step-guide-with-render-810ccbf49573)

[Getting Started with Django on Render](https://docs.render.com/deploy-django#create-a-build-script)

#### 參考資料 - Linebot
[[Python+LINE Bot教學]6步驟快速上手LINE Bot機器人](https://www.learncodewithmike.com/2020/06/python-line-bot.html)

[[Day 2]用Django架構建置專屬的LINEBOT吧 - 開始第一個Django專案](https://ithelp.ithome.com.tw/articles/10238660)

[#新手 line bot python一次回覆多則訊息](https://www.dcard.tw/f/softwareengineer/p/233395114)

[[Django教學7]善用Django ModelForm快速開發CRUD應用程式教學](https://www.learncodewithmike.com/2020/03/django-modelform.html)

[Line Bot 互動式同時回傳 "圖片", "文字", "貼圖"](https://ithelp.ithome.com.tw/articles/10298260?sc=rss.qu)