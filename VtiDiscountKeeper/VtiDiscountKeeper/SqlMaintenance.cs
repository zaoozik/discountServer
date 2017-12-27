using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;
using System.Data;
using System.Data.Common;

namespace VtiDiscountKeeper
{
    static class SqlMaintenance
    {
        private static SQLiteConnection conn = new SQLiteConnection();
        private static bool CONNECTED = false;

        static public void CreateDb(string filename)
        {
            SQLiteConnection.CreateFile(filename);

        }

        static public void Connect(string db_file)
        {
            if (!CONNECTED)
            {

                conn.ConnectionString = "Data Source = " + db_file;
                conn.Open();
                CONNECTED = true;
            }

        }

        static public void Close()
        {

            conn.Close();
            System.Data.SQLite.SQLiteConnection.ClearAllPools();
            CONNECTED = false;

        }

        static public void ExCommand(string command_text)
        {

            SQLiteCommand command = new SQLiteCommand(conn);
            command.CommandText = command_text;
            command.CommandType = CommandType.Text;
            command.ExecuteNonQuery();

        }

        static public SQLiteDataReader ExCommandResult(string command_text)
        {
            SQLiteCommand command = new SQLiteCommand(command_text, conn);
            SQLiteDataReader reader = command.ExecuteReader();
            return reader;

        }



    }
}

