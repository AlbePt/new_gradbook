import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { ArrowLeft, Upload, FileSpreadsheet, Users, BookOpen, CheckCircle, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { UploadFile, ExtractDataFromUploadedFile } from "@/integrations/Core";
import { Student, Teacher, Subject, Class, School } from "@/entities/all";

const ImportStep = ({ number, title, description, isActive, isComplete }) => (
  <div className={`flex items-center gap-4 p-4 rounded-lg transition-all ${
    isActive ? 'bg-blue-50 border-2 border-blue-200' : 
    isComplete ? 'bg-green-50 border-2 border-green-200' : 'bg-white border border-slate-200'
  }`}>
    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${
      isComplete ? 'bg-green-500 text-white' :
      isActive ? 'bg-blue-500 text-white' : 'bg-slate-300 text-slate-600'
    }`}>
      {isComplete ? <CheckCircle className="w-5 h-5" /> : number}
    </div>
    <div>
      <h3 className="font-semibold text-slate-800">{title}</h3>
      <p className="text-sm text-slate-600">{description}</p>
    </div>
  </div>
);

export default function Import() {
  const [currentStep, setCurrentStep] = useState(1);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [importResults, setImportResults] = useState(null);

  const steps = [
    { number: 1, title: "Выбор файлов", description: "Загрузите CSV или Excel файлы с данными" },
    { number: 2, title: "Обработка", description: "Извлечение и проверка данных" },
    { number: 3, title: "Импорт", description: "Сохранение данных в системе" },
    { number: 4, title: "Завершение", description: "Просмотр результатов импорта" }
  ];

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files).filter(
      file => file.type.includes('csv') || file.type.includes('sheet') || file.type.includes('excel')
    );
    setFiles(selectedFiles);
    setError("");
  };

  const processFiles = async () => {
    if (files.length === 0) return;
    
    setUploading(true);
    setCurrentStep(2);
    setProgress(10);
    
    try {
      const results = {
        students: [],
        teachers: [],
        subjects: [],
        classes: []
      };

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        setProgress(20 + (i * 60 / files.length));
        
        // Upload file
        const { file_url } = await UploadFile({ file });
        
        // Determine file type and extract data
        const fileName = file.name.toLowerCase();
        let schema;
        
        if (fileName.includes('студент') || fileName.includes('ученик')) {
          schema = Student.schema();
        } else if (fileName.includes('учител')) {
          schema = Teacher.schema();
        } else if (fileName.includes('предмет')) {
          schema = Subject.schema();
        } else if (fileName.includes('класс')) {
          schema = Class.schema();
        } else {
          // Default to student schema
          schema = Student.schema();
        }
        
        const extractResult = await ExtractDataFromUploadedFile({
          file_url,
          json_schema: {
            type: "object",
            properties: {
              data: {
                type: "array",
                items: schema
              }
            }
          }
        });
        
        if (extractResult.status === "success" && extractResult.output?.data) {
          if (fileName.includes('студент') || fileName.includes('ученик')) {
            results.students.push(...extractResult.output.data);
          } else if (fileName.includes('учител')) {
            results.teachers.push(...extractResult.output.data);
          } else if (fileName.includes('предмет')) {
            results.subjects.push(...extractResult.output.data);
          } else if (fileName.includes('класс')) {
            results.classes.push(...extractResult.output.data);
          }
        }
      }
      
      setProgress(80);
      setCurrentStep(3);
      
      // Import data to database
      let totalImported = 0;
      
      if (results.subjects.length > 0) {
        await Subject.bulkCreate(results.subjects);
        totalImported += results.subjects.length;
      }
      
      if (results.teachers.length > 0) {
        await Teacher.bulkCreate(results.teachers);
        totalImported += results.teachers.length;
      }
      
      if (results.classes.length > 0) {
        await Class.bulkCreate(results.classes);
        totalImported += results.classes.length;
      }
      
      if (results.students.length > 0) {
        await Student.bulkCreate(results.students);
        totalImported += results.students.length;
      }
      
      setProgress(100);
      setCurrentStep(4);
      setImportResults({
        ...results,
        total: totalImported
      });
      setSuccess(`Успешно импортировано ${totalImported} записей`);
      
    } catch (error) {
      setError(`Ошибка при импорте данных: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <Link to={createPageUrl("Dashboard")}>
          <Button variant="outline" size="icon" className="hover-lift">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Импорт данных</h1>
          <p className="text-slate-600 mt-1">Загрузите данные из электронного журнала</p>
        </div>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {steps.map((step) => (
            <ImportStep
              key={step.number}
              {...step}
              isActive={currentStep === step.number}
              isComplete={currentStep > step.number}
            />
          ))}
        </div>
        {uploading && (
          <div className="mt-4">
            <Progress value={progress} className="h-2" />
            <p className="text-sm text-slate-600 mt-2">{progress}% завершено</p>
          </div>
        )}
      </div>

      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="mb-6 border-green-200 bg-green-50">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">{success}</AlertDescription>
        </Alert>
      )}

      {/* File Upload */}
      {currentStep === 1 && (
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <Card className="glass-effect border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5" />
                  Загрузка файлов
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
                  <FileSpreadsheet className="w-16 h-16 mx-auto text-slate-400 mb-4" />
                  <h3 className="text-lg font-semibold text-slate-800 mb-2">
                    Выберите файлы для импорта
                  </h3>
                  <p className="text-slate-600 mb-4">
                    Поддерживаются форматы: CSV, Excel (.xlsx, .xls)
                  </p>
                  <input
                    type="file"
                    multiple
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-input"
                  />
                  <label htmlFor="file-input">
                    <Button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 cursor-pointer">
                      Выбрать файлы
                    </Button>
                  </label>
                </div>
                
                {files.length > 0 && (
                  <div className="mt-6">
                    <h4 className="font-semibold mb-3">Выбранные файлы:</h4>
                    <div className="space-y-2">
                      {files.map((file, index) => (
                        <div key={index} className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                          <FileSpreadsheet className="w-5 h-5 text-green-600" />
                          <span className="font-medium">{file.name}</span>
                          <span className="text-sm text-slate-500">
                            ({(file.size / 1024).toFixed(1)} KB)
                          </span>
                        </div>
                      ))}
                    </div>
                    <Button
                      onClick={processFiles}
                      className="w-full mt-4 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800"
                      disabled={uploading}
                    >
                      Начать обработку
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
          
          <div>
            <Card className="glass-effect border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="text-lg">Требования к файлам</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-semibold text-slate-800 mb-2 flex items-center gap-2">
                    <Users className="w-4 h-4" />
                    Студенты
                  </h4>
                  <p className="text-sm text-slate-600">
                    Имя файла должно содержать "студент" или "ученик"
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold text-slate-800 mb-2 flex items-center gap-2">
                    <BookOpen className="w-4 h-4" />
                    Предметы
                  </h4>
                  <p className="text-sm text-slate-600">
                    Имя файла должно содержать "предмет"
                  </p>
                </div>
                <div className="pt-2 border-t">
                  <p className="text-xs text-slate-500">
                    Убедитесь, что данные в файлах содержат все необходимые поля
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Results */}
      {currentStep === 4 && importResults && (
        <Card className="glass-effect border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-700">
              <CheckCircle className="w-5 h-5" />
              Импорт завершён успешно
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <Users className="w-8 h-8 mx-auto text-blue-600 mb-2" />
                <p className="text-2xl font-bold text-blue-700">{importResults.students.length}</p>
                <p className="text-sm text-blue-600">Студентов</p>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <BookOpen className="w-8 h-8 mx-auto text-green-600 mb-2" />
                <p className="text-2xl font-bold text-green-700">{importResults.subjects.length}</p>
                <p className="text-sm text-green-600">Предметов</p>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <Users className="w-8 h-8 mx-auto text-purple-600 mb-2" />
                <p className="text-2xl font-bold text-purple-700">{importResults.teachers.length}</p>
                <p className="text-sm text-purple-600">Учителей</p>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <Users className="w-8 h-8 mx-auto text-orange-600 mb-2" />
                <p className="text-2xl font-bold text-orange-700">{importResults.classes.length}</p>
                <p className="text-sm text-orange-600">Классов</p>
              </div>
            </div>
            <div className="flex gap-3">
              <Link to={createPageUrl("Dashboard")}>
                <Button variant="outline">
                  Вернуться на главную
                </Button>
              </Link>
              <Link to={createPageUrl("Reports")}>
                <Button className="bg-gradient-to-r from-blue-600 to-indigo-600">
                  Создать отчёт
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

