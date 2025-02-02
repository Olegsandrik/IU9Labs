using System;
using System.Data;
using System.Data.SqlClient;
using System.Threading.Tasks;
using System.Configuration;
using System.Linq;

namespace HelloApp
{
    class Program
    {
        static async Task Main(string[] args)
        {
            try
                {
                // Достаем строчку подключения из App.config
                string connectionString = ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString;

                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();
                    Console.WriteLine("Подключение открыто");
                    // Вывод информации о подключении
                    Console.WriteLine("Свойства подключения:");
                    Console.WriteLine($"\tСтрока подключения: {connection.ConnectionString}");
                    Console.WriteLine($"\tБаза данных: {connection.Database}");
                    Console.WriteLine($"\tСервер: {connection.DataSource}");
                    Console.WriteLine($"\tВерсия сервера: {connection.ServerVersion}");
                    Console.WriteLine($"\tСостояние: {connection.State}");
                    Console.WriteLine($"\tWorkstationld: {connection.WorkstationId}");

                    // реализация задачи лабораторной работы связным уровнем
                    // Вывод уже заготовленной таблицы таблицы
                    await DisplayPolyclinicaTable(connection);

                    Console.WriteLine("ВСТАВКА ДАННЫХ В ТАБЛИЦУ");
                    await InsertPolyclinica(connection, 11, 567832, 3, "Victorenko 11", "Viktorenko11@yandex.ru", "https://Viktorenko.ru", "79228833089");
                    await DisplayPolyclinicaTable(connection);

                    Console.WriteLine("ИЗМЕНЕНИЕ ДАННЫХ В ТАБЛИЦЕ");
                    await UpdatePolyclinica(connection, 11, 0, 0, "UPDATED", "UPDATED");
                    await DisplayPolyclinicaTable(connection);

                    Console.WriteLine("УДАЛЕНИЕ ДАННЫХ ИЗ ТАБЛИЦЫ");
                    await DeletePolyclinica(connection, 11);
                    await DisplayPolyclinicaTable(connection);
                }

                Console.WriteLine("Связное подключение закрыто...");
                Console.WriteLine("Начало работы с несвязным уровнем");
                await Disconected();
                Console.WriteLine("Несвязное подключение закрыто...");
                Console.WriteLine("Программа завершила работу.");
                Console.Read();

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

        }

        static async Task DisplayPolyclinicaTable(SqlConnection connection)
        {
            try
                {
                Console.WriteLine("Вывод таблицы Polyclinica");
                string query = "SELECT PolyclinicID, LicenseNum, BranchNum, AddressMin, Email, WebsiteLink, PhoneNum FROM Polyclinica";
                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            int PolyclinicID = (int)reader["PolyclinicID"];
                            int LicenseNum = (int)reader["LicenseNum"];
                            int BranchNum = (int)reader["BranchNum"];
                            string AddressMin = reader["AddressMin"].ToString();
                            string Email = reader["Email"].ToString();
                            string WebsiteLink = reader["WebsiteLink"].ToString();
                            string PhoneNum = reader["PhoneNum"].ToString();

                            Console.WriteLine($"PolyclinicID: {PolyclinicID}, LicenseNum: {LicenseNum}, BranchNum: {BranchNum}" +
                                $", AddressMin: {AddressMin}, Email: {Email}, WebsiteLink: {WebsiteLink}, PhoneNum: {PhoneNum}");
                        }
                    }
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

        }

        static async Task InsertPolyclinica(SqlConnection connection, int id, int licenseNum, int branchNum, string address, string email, string website, string phone)
        {
            try
            {
                string sqlExpressionInsert = "INSERT INTO Polyclinica (PolyclinicID, LicenseNum, BranchNum, AddressMin, Email, WebsiteLink, PhoneNum) " +
                                          "VALUES (@PolyclinicID, @LicenseNum, @BranchNum, @AddressMin, @Email, @WebsiteLink, @PhoneNum);";

                using (SqlCommand commandForInsert = new SqlCommand(sqlExpressionInsert, connection))
                {
                    commandForInsert.Parameters.AddWithValue("@PolyclinicID", id);
                    commandForInsert.Parameters.AddWithValue("@LicenseNum", licenseNum);
                    commandForInsert.Parameters.AddWithValue("@BranchNum", branchNum);
                    commandForInsert.Parameters.AddWithValue("@AddressMin", address);
                    commandForInsert.Parameters.AddWithValue("@Email", email);
                    commandForInsert.Parameters.AddWithValue("@WebsiteLink", website);
                    commandForInsert.Parameters.AddWithValue("@PhoneNum", phone);

                    int numberInsert = await commandForInsert.ExecuteNonQueryAsync();
                    Console.WriteLine($"Добавлено объектов: {numberInsert}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task UpdatePolyclinica(SqlConnection connection, int id, int licenseNum, int branchNum, string address, string email)
        {
            try
                {
                string sqlExpressionUpdate = "UPDATE Polyclinica SET LicenseNum = @LicenseNum, BranchNum = @BranchNum, AddressMin = @AddressMin, Email = @Email " +
                                              "WHERE PolyclinicID = @PolyclinicID";

                using (SqlCommand commandForUpdate = new SqlCommand(sqlExpressionUpdate, connection))
                {
                    commandForUpdate.Parameters.AddWithValue("@PolyclinicID", id);
                    commandForUpdate.Parameters.AddWithValue("@LicenseNum", licenseNum);
                    commandForUpdate.Parameters.AddWithValue("@BranchNum", branchNum);
                    commandForUpdate.Parameters.AddWithValue("@AddressMin", address);
                    commandForUpdate.Parameters.AddWithValue("@Email", email);

                    int numberUpdate = await commandForUpdate.ExecuteNonQueryAsync();
                    Console.WriteLine($"Обновлено объектов: {numberUpdate}");
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task DeletePolyclinica(SqlConnection connection, int id)
        {
            try
                {
                string sqlExpressionDelete = "DELETE FROM Polyclinica WHERE PolyclinicID = @PolyclinicID";

                using (SqlCommand command = new SqlCommand(sqlExpressionDelete, connection))
                {
                    command.Parameters.AddWithValue("@PolyclinicID", id);
                    int numberDelete = await command.ExecuteNonQueryAsync();
                    Console.WriteLine($"Удалено объектов: {numberDelete}");
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

        }

        static async Task Disconected()
        {
            try
                {

                string connectionString = ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString;

                DataSet dataSet = new DataSet();

                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    
                    string query = "SELECT PolyclinicID, LicenseNum, BranchNum, AddressMin, Email, WebsiteLink, PhoneNum FROM Polyclinica";
                    using (SqlDataAdapter dataAdapter = new SqlDataAdapter(query, connection))
                    {
                        await Task.Run(() => dataAdapter.Fill(dataSet, "Polyclinica"));
                    }

                    DataTable table = dataSet.Tables["Polyclinica"];
                    DisplayData(table);

                    // вставка записи в DataSet
                    Console.WriteLine("Вставка в Dataset");
                    InsertRowToDataSet(table, 11, 567832, 3, "Viktorenko 11", "Viktorenko11@yandex.ru", "https://Viktorenko.ru", "79228833089");
                    // InsertRowToDataSet(table, 16, 567832, 3, "Viktorenko 11", "Viktorenko11@yandex.ru", "https://Viktorenko.ru", "79228833089");
                    DisplayData(table);

                    // изменение записи
                    Console.WriteLine("Изменение в Dataset");
                    UpdateRowInDataSet(table, 11, 0, 0, "Updated", "Updated");
                    // UpdateRowInDataSet(table, 15, 0, 0, "Updated", "Updated");
                    DisplayData(table);

                    // Удаление записи
                    Console.WriteLine("Удаление в Dataset");
                    DeleteRowFromDataSet(table, 11);
                    DeleteRowFromDataSet(table, 16);
                    DisplayData(table);
                    // CheckForChanges(table);

                    // сохранение изменений в БД
                    await connection.OpenAsync();
                    await SaveChangesToDatabase(connection, table);

                    Console.WriteLine("Финальная проверка данных в БД");
                    await DisplayPolyclinicaTable(connection);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

        }

        static void InsertRowToDataSet(DataTable table, int id, int licenseNum, int branchNum, string address, string email, string website, string phone)
        {
            DataRow newRow = table.NewRow();
            newRow["PolyclinicID"] = id;
            newRow["LicenseNum"] = licenseNum;
            newRow["BranchNum"] = branchNum;
            newRow["AddressMin"] = address;
            newRow["Email"] = email;
            newRow["WebsiteLink"] = website;
            newRow["PhoneNum"] = phone;
            table.Rows.Add(newRow);
        }

        static void UpdateRowInDataSet(DataTable table, int id, int licenseNum, int branchNum, string address, string email)
        {
            DataRow existingRow = table.Select($"PolyclinicID = {id}").FirstOrDefault();
            if (existingRow != null)
            {
                existingRow["BranchNum"] = branchNum;
                existingRow["LicenseNum"] = licenseNum;
                existingRow["AddressMin"] = address;
                existingRow["Email"] = email;
                Console.WriteLine("Изменена существующая запись.");
            }
        }

        static void DeleteRowFromDataSet(DataTable table, int id)
        {
            DataRow rowToDelete = table.Select($"PolyclinicID = {id}").FirstOrDefault();
            if (rowToDelete != null)
            {
                table.Rows.Remove(rowToDelete);
                Console.WriteLine("Запись удалена.");
                Console.WriteLine(rowToDelete.RowState);
            }
        }

        static async Task SaveChangesToDatabase(SqlConnection connection, DataTable table)
        {
            try
            {
                DataTable changes = table.GetChanges();
                Console.WriteLine(changes);
                if (changes != null)
                {
                    foreach (DataRow row in changes.Rows)
                    {
                        if (row.RowState == DataRowState.Added)
                        {
                            await InsertPolyclinica(connection,
                                (int)row["PolyclinicID"],
                                (int)row["LicenseNum"],
                                (int)row["BranchNum"],
                                row["AddressMin"].ToString(),
                                row["Email"].ToString(),
                                row["WebsiteLink"].ToString(),
                                row["PhoneNum"].ToString());
                        }
                        else if (row.RowState == DataRowState.Modified)
                        {
                            await UpdatePolyclinica(connection,
                                (int)row["PolyclinicID"],
                                (int)row["LicenseNum"],
                                (int)row["BranchNum"],
                                row["AddressMin"].ToString(),
                                row["Email"].ToString());
                        }
                        else if (row.RowState == DataRowState.Detached || row.RowState == DataRowState.Deleted)
                        {
                            await DeletePolyclinica(connection, (int)row["PolyclinicID"]);
                        }
                    }

                    table.AcceptChanges();
                }
                else
                {
                    Console.WriteLine("Нет изменений для сохранения.");
                }

            }
            catch (Exception ex) { 
                Console.WriteLine(ex.Message);
            }
        }


        static void DisplayData(DataTable table)
        {
            Console.WriteLine("Вывод таблицы Polyclinica из DataSet:");
            foreach (DataRow row in table.Rows)
            {
                Console.WriteLine($"PolyclinicID: {row["PolyclinicID"]}, LicenseNum: {row["LicenseNum"]}, BranchNum: {row["BranchNum"]}, " +
                    $"AddressMin: {row["AddressMin"]}, Email: {row["Email"]}, WebsiteLink: {row["WebsiteLink"]}, PhoneNum: {row["PhoneNum"]}");
            }
            Console.WriteLine();
        }
    }
}
