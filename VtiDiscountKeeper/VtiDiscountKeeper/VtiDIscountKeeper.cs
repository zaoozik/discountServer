using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Http;
using System.IO;
using System.Collections.Specialized;
using System.Data.SQLite;
using System.Data.Common;
using System.Threading;
using System.Timers;
using System.Configuration;

namespace VtiDiscountKeeper
{
    public partial class VtiDiscountKeeper : ServiceBase
    {
        public VtiDiscountKeeper()
        {
            InitializeComponent();

        }


        static HttpListener listener = new HttpListener();
        private static readonly HttpClient client = new HttpClient();
        private static string DB_NAME = System.AppDomain.CurrentDomain.BaseDirectory + @"vtikeeper.db3";
        private static string LOG_FILE = System.AppDomain.CurrentDomain.BaseDirectory + @"keeper.log";



        static void Listen()
        {

            var appSettings = System.Configuration.ConfigurationSettings.AppSettings;
            string port = "8888";
            try
            {
                if (appSettings["serviceListenPort"] != null)
                {
                    port = appSettings["serviceListenPort"];
                }
            }
            catch
            {
                port = "8888";
            }



            listener.Prefixes.Add("http://localhost:"+port+"/");
            listener.Start();
            Task.Factory.StartNew(() =>
            {
                while (true)
                {

                    IAsyncResult result = listener.BeginGetContext(new AsyncCallback(ListenerCallback), listener);
                    result.AsyncWaitHandle.WaitOne();
                }
            });

            

        }



        public static void ListenerCallback(IAsyncResult result)
        {
            HttpListener listener = (HttpListener)result.AsyncState;
            // Call EndGetContext to complete the asynchronous operation.
            HttpListenerContext context = listener.EndGetContext(result);
            HttpListenerRequest request = context.Request;
            // Obtain a response object.
            HttpListenerResponse response = context.Response;
            // Construct a response.


            string responseString = "";

            if (request.HttpMethod == "POST")
            {
                System.IO.Stream body = request.InputStream;
                System.IO.StreamReader reader = new System.IO.StreamReader(body, Encoding.UTF8);


                string rec = reader.ReadToEnd(); 
                try
                {

                    string curr_path = Directory.GetCurrentDirectory();
                    SqlMaintenance.Connect(DB_NAME);
                    string sql = String.Format("INSERT INTO t_data (post_data, datetime) VALUES ('{0}', '{1}')", rec, DateTime.Now);
                    SqlMaintenance.ExCommand(sql);
                    SqlMaintenance.Close();
                    response.StatusCode = 200;

                    var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                    byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] Получено сообщение {1}{2}", DateTime.Now, rec, Environment.NewLine));
                    log.Write(log_rec, 0, log_rec.Length);
                    log.Close();
                }
                catch (Exception ex)
                {
                    SqlMaintenance.Close();
                    var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                    byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] ОШИБКА В ПОЛУЧЕНИИ {1}{2}", DateTime.Now, ex, Environment.NewLine));
                    log.Write(log_rec, 0, log_rec.Length);
                    log.Close();
                    response.StatusCode = 500;
                }


                responseString = "1";
                response.ContentType = "text/plain";
                response.Headers.Add("Date", String.Empty);
                response.ContentEncoding = request.ContentEncoding;
                byte[] buffer = System.Text.Encoding.GetEncoding(1251).GetBytes(responseString);
                response.ContentLength64 = buffer.Length;
                Stream output = response.OutputStream;
                output.Write(buffer, 0, buffer.Length);
                response.Close();
            }

            if (request.HttpMethod == "GET")
            {
                responseString = "<html><head></head><body><h1>VTI Discount SERVICE</h1>" +
                    "<p>normal load</p>" +
                    "<p>its works!</p>" +
                    "</body></html>";
                response.ContentType = "text/html";
                response.StatusCode = 200;
                response.Headers.Add("Date", String.Empty);
                response.ContentEncoding = request.ContentEncoding;
                byte[] buffer = System.Text.Encoding.GetEncoding(1251).GetBytes(responseString);
                response.ContentLength64 = buffer.Length;
                Stream output = response.OutputStream;
                output.Write(buffer, 0, buffer.Length);
                response.Close();
            }
    }


        public static void Post(object obj, ElapsedEventArgs e)
        {
            try
                {
                        var appSettings = System.Configuration.ConfigurationSettings.AppSettings;
                        string server = "http://77.243.11.250:1024/";
                        try
                        {
                            if (appSettings["discountServerAddress"] != null)
                            {
                                server = appSettings["discountServerAddress"];
                            }
                        }
                        catch
                        {
                           server = "http://77.243.11.250:1024/";
                        }


                SqlMaintenance.Connect(DB_NAME);
                    string sql = "SELECT * FROM t_data";
                    var reader = SqlMaintenance.ExCommandResult(sql);

                    string post_data;
                    string date;
                List<Dictionary<String, String>> data_ar = new  List<Dictionary<String, String>>();

                foreach (DbDataRecord record in reader)
                    {
                        Dictionary<String, String> rec = new Dictionary<String, String>();
                        post_data = record["post_data"].ToString();
                        date = record["datetime"].ToString();
                        post_data += "&datetime=" + date;
                        post_data += "&vtikeeper=token";
                    rec.Add("post", post_data);
                    rec.Add("id", record["id"].ToString());
                    data_ar.Add(rec);
                    }

                    reader.Close();
                    SqlMaintenance.Close();

                foreach (var record in data_ar)
                    {        

                    var hcon = new StringContent(record["post"]);
                        hcon.Headers.Clear();
                        hcon.Headers.Add("Content-Type","application/x-www-form-urlencoded");

                        var response =  client.PostAsync(server + "api/cards/vti_keeper/", hcon).Result;
                        HttpStatusCode status = response.StatusCode;
                        if (status == HttpStatusCode.OK)
                        {
                            SqlMaintenance.Connect(DB_NAME);
                            sql = "DELETE FROM t_data WHERE id=" + record["id"];
                            SqlMaintenance.ExCommand(sql);
                            SqlMaintenance.Close();

                        var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                            byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] Отправка на сервер {1}{2}", DateTime.Now, record["post"], Environment.NewLine));
                            log.Write(log_rec, 0, log_rec.Length);
                            log.Close();
                        }

                    }
                    
                }
                catch (Exception ex)
                {
                    SqlMaintenance.Close();
                    var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                    byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] ОШИБКА В ОТПРАВКЕ {1}{2}", DateTime.Now, ex, Environment.NewLine));
                    log.Write(log_rec, 0, log_rec.Length);
                    log.Close();
            }

        }


        public static void Test()
        {

            var appSettings = System.Configuration.ConfigurationSettings.AppSettings;
            string server = "http://192.168.0.24/";
            try
            {
                if (appSettings["discountServerAddress"] != null)
                {
                    server = appSettings["discountServerAddress"];
                }
            }
            catch
            {
                server = "http://192.168.0.24/";
            }


            try
            {
                SqlMaintenance.Connect(DB_NAME);
                string sql = "SELECT * FROM t_data";
                var reader = SqlMaintenance.ExCommandResult(sql);
                reader.Close();
                SqlMaintenance.Close();

                var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] Тест БД пройден успешно! {1}", DateTime.Now, Environment.NewLine));
                log.Write(log_rec, 0, log_rec.Length);
                log.Close();

            }
            catch (Exception ex)
            {
                SqlMaintenance.Close();
                var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] Тест БД НЕ ПРОЙДЕН! {1}{2}", DateTime.Now, ex, Environment.NewLine));
                log.Write(log_rec, 0, log_rec.Length);
                log.Close();
            }

            try
            { 
                 var response = client.GetAsync(server).Result;
                HttpStatusCode status = response.StatusCode;
                if (status == HttpStatusCode.OK)
                {

                    var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                    byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] Тест связи с дисконтным сервером успешно пройден! {1}", DateTime.Now, Environment.NewLine));
                    log.Write(log_rec, 0, log_rec.Length);
                    log.Close();
                }
                else
                {
                    var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                    byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] Тест связи с дисконтным сервером НЕ ПРОЙДЕН! Не вернул 200. Статус - {1}{2}", DateTime.Now, status, Environment.NewLine));
                    log.Write(log_rec, 0, log_rec.Length);
                    log.Close();
                }

            }
            catch (Exception ex)
            {
                var log = File.Open(LOG_FILE, FileMode.Append, FileAccess.Write);
                byte[] log_rec = System.Text.Encoding.GetEncoding(1251).GetBytes(String.Format("[{0}] Тест связи с дисконтным сервером не пройден! Ошибка - {1}{2}", DateTime.Now, ex, Environment.NewLine));
                log.Write(log_rec, 0, log_rec.Length);
                log.Close();
            }

        }


        protected override  void OnStart(string[] args)
        {

            var log = File.Open(LOG_FILE, FileMode.Create, FileAccess.Write);
            log.Close();

            Test();
            Listen();
            var timer = new System.Timers.Timer(60000);
            timer.Elapsed += Post;
            timer.Enabled = true;
            timer.Start();
            object obj = new object();
            ElapsedEventArgs e = null;
       
            Post(obj, e);

        }


        protected override void OnStop()
        {
            listener.Stop();
        }
    }
}
