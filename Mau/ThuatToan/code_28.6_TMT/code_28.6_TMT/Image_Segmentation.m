function varargout = Image_Segmentation(varargin)
% IMAGE_SEGMENTATION MATLAB code for Image_Segmentation.fig
%      IMAGE_SEGMENTATION, by itself, creates a new IMAGE_SEGMENTATION or raises the existing
%      singleton*.
%
%      H = IMAGE_SEGMENTATION returns the handle to a new IMAGE_SEGMENTATION or the handle to
%      the existing singleton*.
%
%      IMAGE_SEGMENTATION('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in IMAGE_SEGMENTATION.M with the given input arguments.
%
%      IMAGE_SEGMENTATION('Property','Value',...) creates a new IMAGE_SEGMENTATION or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Image_Segmentation_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Image_Segmentation_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Image_Segmentation

% Last Modified by GUIDE v2.5 01-Jul-2015 21:59:52

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Image_Segmentation_OpeningFcn, ...
                   'gui_OutputFcn',  @Image_Segmentation_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before Image_Segmentation is made visible.
function Image_Segmentation_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Image_Segmentation (see VARARGIN)

% Choose default command line output for Image_Segmentation
handles.output = hObject;

set(handles.num_of_clust, 'enable', 'off');
set(handles.exponent, 'enable', 'off');
set(handles.epsilon, 'enable', 'off');
set(handles.max_num_iter, 'enable', 'off');
% set(handles.btn_seg_fcm_otsu, 'enable', 'off');

% set(handles.alg_resl_panel, 'visible', 'off');
% set(handles.org_img_panel, 'visible', 'off');
set(handles.fcm_img_panel, 'visible', 'off');
set(handles.otsu_img_panel, 'visible', 'off');
set(handles.final_img_panel, 'visible', 'off');
% Update handles structure
guidata(hObject, handles);


% UIWAIT makes Image_Segmentation wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Image_Segmentation_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in btn_open.
function btn_open_Callback(hObject, eventdata, handles)
% hObject    handle to btn_open (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[filename, pathname] = uigetfile({'*.jpg'}, 'Pick a deltal X - ray image');
 
% set(handles.alg_resl_panel, 'visible', 'off');
set(handles.result_panel, 'visible', 'off');
set(handles.algorithms_panel, 'visible', 'off');

if filename ~= 0
%     set(handles.open_file,'string', filename);
   
    IM = imread([pathname, filename]);
    
%     imfinfo([pathname, filename])
    
%     set(handles.org_img_panel, 'visible', 'on');
      
    axes(handles.original_img);
    imshow(IM);
    
    handles.num_of_data_point = size(IM(:, : , 1), 1) * size(IM(:, : , 1), 2);
    handles.filename = filename;
    
    
%     set(handles.btn_seg_fcm_otsu, 'enable', 'on');
    
    set(handles.original_img,'UserData',IM);
    set(handles.otsu_img_panel, 'visible', 'on');
    
    set(handles.num_of_clust, 'enable', 'on');
    set(handles.num_of_clust,'UserData', 5);
    set(handles.num_of_clust,'string', '5');
        
    set(handles.exponent, 'enable', 'on');
    set(handles.exponent,'UserData', 2);
    set(handles.exponent,'string', '2');
    
    set(handles.epsilon, 'enable', 'on');
    set(handles.epsilon,'UserData', 0.005);
    set(handles.epsilon,'string', '0.005');
    
    set(handles.max_num_iter, 'enable', 'on');
    set(handles.max_num_iter,'UserData', 150);
    set(handles.max_num_iter,'string', '150');
else
%     set(handles.open_file,'string', 'No file is chosen.');
    set(handles.num_of_clust, 'enable', 'off');
    set(handles.exponent, 'enable', 'off');
    set(handles.epsilon, 'enable', 'off');
    set(handles.max_num_iter, 'enable', 'off');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'off');
    
%     set(handles.org_img_panel, 'visible', 'off');
end
 set(handles.fcm_img_panel, 'visible', 'off');
 set(handles.final_img_panel, 'visible', 'off');
guidata(hObject, handles);


% --- Executes on button press in btn_close.
function btn_close_Callback(hObject, eventdata, handles)
% hObject    handle to btn_close (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
close;


function open_file_Callback(hObject, eventdata, handles)
% hObject    handle to open_file (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of open_file as text
%        str2double(get(hObject,'String')) returns contents of open_file as a double


% --- Executes during object creation, after setting all properties.
function open_file_CreateFcn(hObject, eventdata, handles)
% hObject    handle to open_file (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function num_of_clust_Callback(hObject, eventdata, handles)
% hObject    handle to num_of_clust (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_of_clust as text
%        str2double(get(hObject,'String')) returns contents of num_of_clust as a double

str = get(hObject,'string');
data = str2double(str);
if isnan(data) || data < 1 || data >  15 || data ~= round(data)
    errordlg(strcat('The number of clusters must be a positive integer and should be less than 15'), 'Bad input');
    set(hObject,'BackgroundColor','y');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'off');
else
    set(hObject,'BackgroundColor','w');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'on');
    set(hObject,'UserData',data);
end
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function num_of_clust_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_of_clust (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function exponent_Callback(hObject, eventdata, handles)
% hObject    handle to exponent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of exponent as text
%        str2double(get(hObject,'String')) returns contents of exponent as a double

str = get(hObject,'string');
data = str2double(str);
if isnan(data) || data < 1
    errordlg('The weighting exponent must be a positive number', 'Bad input');
    set(hObject,'BackgroundColor','y');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'off');
else
    set(hObject,'BackgroundColor','w');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'on');
    set(hObject,'UserData',data);
end
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function exponent_CreateFcn(hObject, eventdata, handles)
% hObject    handle to exponent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function epsilon_Callback(hObject, eventdata, handles)
% hObject    handle to epsilon (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of epsilon as text
%        str2double(get(hObject,'String')) returns contents of epsilon as a double

str = get(hObject,'string');
data = str2double(str);
if isnan(data) || data < 0
    errordlg('The minimum amount of improvement (eps) must be greater than 0. Example: 0.01, 0.006...', 'Bad input');
    set(hObject,'BackgroundColor','y');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'off');
else
    set(hObject,'BackgroundColor','w');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'on');
    set(hObject,'UserData',data);
end
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function epsilon_CreateFcn(hObject, eventdata, handles)
% hObject    handle to epsilon (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function max_num_iter_Callback(hObject, eventdata, handles)
% hObject    handle to max_num_iter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of max_num_iter as text
%        str2double(get(hObject,'String')) returns contents of max_num_iter as a double

str = get(hObject,'string');
data = str2double(str);
if isnan(data) || data < 0 || data ~= round(data)
    errordlg('The maximum number of iterations must be a positive integer and greater than 0. Example: 50, 100, 200...', 'Bad input');
    set(hObject,'BackgroundColor','y');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'off');
else
    set(hObject,'BackgroundColor','w');
%     set(handles.btn_seg_fcm_otsu, 'enable', 'on');
    set(hObject,'UserData',data);
end
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function max_num_iter_CreateFcn(hObject, eventdata, handles)
% hObject    handle to max_num_iter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in result_popupmenu.
function result_popupmenu_Callback(hObject, eventdata, handles)
% hObject    handle to result_popupmenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns result_popupmenu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from result_popupmenu


% --- Executes during object creation, after setting all properties.
function result_popupmenu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to result_popupmenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in btn_ok_result.
function btn_ok_result_Callback(hObject, eventdata, handles)
% hObject    handle to btn_ok_result (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% fig = figure;
% tbl = uitable('Parent', fig);
% openfig resultGUI.fig
selected_index = get(handles.result_popupmenu, 'Value');
list = get(handles.result_popupmenu, 'String');
selected_string = list {selected_index};

switch selected_string
    case 'Objective function'
        msgbox(sprintf('Min of Objective function is: %.6f', handles.obj_fcn), 'Objective function');
    case 'Centers'
        str = '';
        for i = 1:1:get(handles.num_of_clust,'UserData')
            str = strcat(str, sprintf('\n\nCenter %2d: %20.2f %20.2f %20.2f', i, handles.center(i, 1), handles.center(i, 2), handles.center(i, 3)));
        end
        msgbox(str, 'Center of clusters');
    case 'Membership matrix'
        f = figure('Name', 'Membership matrix', 'NumberTitle','off', 'Position',[300 300 500 250]);
        t = uitable(f);
        set(t, 'Data', handles.U, 'Position',[10 10 480 230]);
%         msgbox(num2str(handles.U, '%10f'), 'Membership matrix'); 
    case 'Time (sec)'
        msgbox(sprintf('Time (sec): %f', handles.elapsed_time), 'Time');
    case 'Davies–Bouldin (DB)'
        DB_value = ValidityIndex('DB', handles.data, get(handles.num_of_clust,'UserData'), handles.center, handles.U);
        msgbox(sprintf('DB value: %f', DB_value), 'DB value');
    case 'IFV'
        IFV_value = ValidityIndex('IFV', handles.data, get(handles.num_of_clust,'UserData'), handles.center, handles.U);
        msgbox(sprintf('IFV value: %f', IFV_value), 'IFV value');
    case 'PBM' 
        PBM_value = ValidityIndex('PBM', handles.data, get(handles.num_of_clust,'UserData'), handles.center, handles.U);
        msgbox(sprintf('PBM value: %f', PBM_value), 'PBM value');
    case 'Silhouette width criterion (SWC)'
        SWC_value = ValidityIndex('SWC', handles.data, get(handles.num_of_clust,'UserData'), handles.center, handles.U);
        msgbox(sprintf('Silhouette width criterion (SWC) value: %f', SWC_value), 'SWC value');
end


% --- Executes on button press in btn_otsu_filter.
function btn_otsu_filter_Callback(hObject, eventdata, handles)
% hObject    handle to btn_otsu_filter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
  
set(handles.fcm_img_panel, 'visible', 'off');
set(handles.final_img_panel, 'visible', 'off');
set(handles.result_panel, 'visible', 'off');
set(handles.algorithms_panel, 'visible', 'off');

x = inputdlg('Enter number of threshold (>= 1):', 'Otsu');

numThresh = str2num(x{:});

if isnan(numThresh) || numThresh < 0 || numThresh ~= round(numThresh)
    errordlg('The number of threshold must be a positive integer. Example: 1,2,3...', 'Bad input');
else
    IM = get(handles.original_img, 'UserData');
    
    tic;
    thresh = multithresh(IM, numThresh);
    value = [0 thresh(2:end) 255];
    thresh_img = imquantize(IM, thresh, value);
    handles.elapsed_time = toc;
   
    axes(handles.otsu_img);
    imshow(thresh_img);
    
    [data, row, column] = input(IM);
    
    data_mean_RGB = mean(data, 2);
    
    U = zeros(numThresh + 1, row * column);
    V = zeros(numThresh + 1, 3);
    
    index = data_mean_RGB <= thresh(1);
    U(1, :) = index;
    data_clust = data(index, :);
    V(1, :) = mean(data_clust);
    
    index = data_mean_RGB > thresh(end);
    U(numThresh + 1, :) = index;
    data_clust = data(index, :);
    V(numThresh + 1, :) = mean(data_clust);
    
    for i = 2:numThresh
       index = (data_mean_RGB > thresh(i-1)) & (data_mean_RGB <= thresh(i));
       U(i, :) = index;
       data_clust = data(index, :);
       V(i, :) = mean(data_clust);
    end
    
    handles.U = U;
    handles.center = V;
    handles.data= data;
    
    
    set(handles.result_panel, 'visible', 'on');
    set(handles.otsu_img,'UserData',thresh_img);
    
    set(handles.fcm_img_panel, 'visible', 'on');
end
guidata(hObject, handles);

% --- Executes on button press in btn_level_set.
function btn_level_set_Callback(hObject, eventdata, handles)
% hObject    handle to btn_level_set (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    set(handles.fcm_img_panel, 'visible', 'off');
    set(handles.final_img_panel, 'visible', 'off');
    set(handles.result_panel, 'visible', 'off');
    set(handles.algorithms_panel, 'visible', 'off');

    IM = get(handles.original_img, 'UserData');

    tic;
    axes(handles.otsu_img);
    Img_corrected = level_set(IM);
    size(Img_corrected)
    handles.elapsed_time = toc;

    [data, row, column] = input(IM);
    data_mean_RGB = mean(data, 2);
    
    numClust = get(handles.num_of_clust,'UserData');
    
    U = zeros(numClust, row * column);
    V = zeros(numClust, 3);
    thresh = zeros(1, numClust - 1);
    
    for i = 1: (numClust-1)
        thresh(i) = uint8(255/numClust * i);
    end
    
%     thresh
    
    index = data_mean_RGB <= thresh(1);
    U(1, :) = index;
    data_clust = data(index, :);
    V(1, :) = mean(data_clust);
    
    index = data_mean_RGB > thresh(end);
    U(numClust, :) = index;
    data_clust = data(index, :);
    V(numClust, :) = mean(data_clust);
    
    for i = 2:(numClust-1)
       index = (data_mean_RGB > thresh(i-1)) & (data_mean_RGB <= thresh(i));
       U(i, :) = index;
       data_clust = data(index, :);
       V(i, :) = mean(data_clust);
    end
    
    handles.U = U;
    handles.center = V;
%     V
    handles.data = data;
    
    set(handles.fcm_img_panel, 'visible', 'on');
    set(handles.result_panel, 'visible', 'on');
    set(handles.otsu_img,'UserData',Img_corrected);
    
    guidata(hObject, handles);

% --- Executes on button press in btn_seg_fcm_otsu.
function btn_seg_fcm_otsu_Callback(hObject, eventdata, handles)
% hObject    handle to btn_seg_fcm_otsu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% msgbox('Pleaze enter arguments (K, m, eps, maxStep) for this step in Input arguments panel!');

% set(handles.fcm_img_panel, 'visible', 'off');
set(handles.final_img_panel, 'visible', 'off');
set(handles.result_panel, 'visible', 'off');
set(handles.algorithms_panel, 'visible', 'off');
% set(handles.alg_resl_panel, 'visible', 'off');

% set(handles.num_of_clust, 'enable', 'off');
% set(handles.exponent, 'enable', 'off');
% set(handles.epsilon, 'enable', 'off');
% set(handles.max_num_iter, 'enable', 'off');
% set(handles.btn_open, 'enable', 'off');

IM = get(handles.otsu_img, 'UserData');

[data, row, column] = input(IM);

numClust = get(handles.num_of_clust,'UserData');
exponent = get(handles.exponent,'UserData');
epsilon = get(handles.epsilon, 'UserData');
max_iter = get(handles.max_num_iter,'UserData');

opts = [exponent; max_iter; epsilon; 0];

global h;
h = waitbar(0, 'Processing...', 'Position', [250, 200, 270, 50]);

tic;
[center, U, obj_fcn] = FCM(data, numClust, opts);
%[center, U, obj_fcn] = FCMChuan(data, numClust, exponent, epsilon, max_iter);
handles.elapsed_time = toc;

handles.obj_fcn = obj_fcn(size(obj_fcn, 1));
handles.center = center;
handles.U = U;
handles.data = data;

image_out = output(data, numClust, U, row, column);

axes(handles.fcm_img);
imshow(image_out);

set(handles.final_img_panel, 'visible', 'on');
set(handles.result_panel, 'visible', 'on');
set(handles.algorithms_panel, 'visible', 'on');
% set(handles.btn_open, 'enable', 'on');

imwrite(image_out, ['Output_FCM_otsu_' handles.filename]);
guidata(hObject, handles);

% --- Executes on button press in btn_seg_fcm_org.
function btn_seg_fcm_org_Callback(hObject, eventdata, handles)
% hObject    handle to btn_seg_fcm_org (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
set(handles.final_img_panel, 'visible', 'off');
set(handles.result_panel, 'visible', 'off');
set(handles.algorithms_panel, 'visible', 'off');

IM = get(handles.original_img, 'UserData');

[data, row, column] = input(IM);

numClust = get(handles.num_of_clust,'UserData');
exponent = get(handles.exponent,'UserData');
epsilon = get(handles.epsilon, 'UserData');
max_iter = get(handles.max_num_iter,'UserData');

opts = [exponent; max_iter; epsilon; 0];

global h;
h = waitbar(0, 'Processing...', 'Position', [250, 200, 270, 50]);

tic;
[center, U, obj_fcn] = FCM(data, numClust, opts);

%[center, U, obj_fcn] = FCMChuan(data, numClust, exponent, epsilon, max_iter);
handles.elapsed_time = toc;

handles.obj_fcn = obj_fcn(size(obj_fcn, 1));
handles.center = center;
handles.U = U;
handles.data = data;

image_out = output(data, numClust, U, row, column);

% set(handles.fcm_img_panel, 'visible', 'on');
axes(handles.fcm_img);
imshow(image_out);

set(handles.final_img_panel, 'visible', 'on');
set(handles.result_panel, 'visible', 'on');
set(handles.algorithms_panel, 'visible', 'on');
% set(handles.btn_open, 'enable', 'on');

imwrite(image_out, ['Output_FCM_org_' handles.filename]);
guidata(hObject, handles);


% --- Executes on button press in btn_segment_semi.
function btn_segment_semi_Callback(hObject, eventdata, handles)
% hObject    handle to btn_segment_semi (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

C = get(handles.num_of_clust,'UserData');
m = get(handles.exponent,'UserData');
Eps = get(handles.epsilon, 'UserData');
maxTest = get(handles.max_num_iter,'UserData');

U1 = handles.U;

IM = get(handles.original_img, 'UserData');
[X, row, column] = input(IM);

selected_index = get(handles.algorithms_popupmenu, 'Value');
list = get(handles.algorithms_popupmenu, 'String');
selected_string = list {selected_index};

global h;
h = waitbar(0, 'Processing...', 'Position', [250, 200, 270, 50]);

switch selected_string
    case 'SSSFC'
        tic;
        [V,U,J]=SSSFC(X,C,m,Eps,maxTest,U1);
        handles.elapsed_time = toc;
        
        image_out = output(X, C, U, row, column);
        imwrite(image_out, ['Output_SSSFC_' handles.filename]);
        
    case 'eSFCM'
       % nhap tham so
      % x = inputdlg('Enter lamda:', 'eSFCM');
       %lamda = str2num(x{:});
        tic;
        [V,U,J]=eSFCM(X,C,m,Eps,maxTest,U1);
        handles.elapsed_time = toc;
        
        image_out = output(X, C, U, row, column);
        imwrite(image_out, ['Output_eSFCM _' handles.filename]);
        
    case 'SSFCMBP' 
%       nhap tham so
%        x = inputdlg('Enter H:', 'SSFCMBP');
%        H = str2num(x{:});
%       Kiem tra tham so
%        if isnan(H) || H < 0 || H ~= round(H)
%            errordlg('H must be a positive integer. Example: 1,2,3...', 'Bad input');
%        else
        tic;
        [V,U,J]= SSFCMBP(X,C,m,Eps,maxTest,U1);
        handles.elapsed_time = toc;
        
        image_out = output(X, C, U, row, column);
        imwrite(image_out, ['Output_SSFCMBP_' handles.filename]);
 %       end     
end

handles.center = V;
handles.U = U;
handles.obj_fcn = J;

axes(handles.final_img);
imshow(image_out);

guidata(hObject, handles);


% --- Executes on selection change in algorithms_popupmenu.
function algorithms_popupmenu_Callback(hObject, eventdata, handles)
% hObject    handle to algorithms_popupmenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns algorithms_popupmenu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from algorithms_popupmenu


% --- Executes during object creation, after setting all properties.
function algorithms_popupmenu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to algorithms_popupmenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function [data, row, column] = input(IM)
R = IM(:, : , 1);
G = IM(:, : , 2);
B = IM(:, : , 3);

row = size(R,1);
column = size(R, 2);

data = double ([R(:) G(:) B(:)]); 


function image_out = output(data, numClust, U, row, column)
color = [0 0 0;  255 255 255;  0 0 255;  0 255 0; 236 135 14;
        152	208	185;  255 0 0;
        255 255 0; 255 0 255; 245 168 154; 148	83	5; 
        156	153	0; 54 117 23;  0	98	65; 175	215	136;
        16	54	103; 81	31	144; 160 149 196; 197 124 172; 215	215	215];

maxU = max(U);
for i = 1 : numClust
    index = find(U(i,:) == maxU);
    for j = index
        data(j, :) = color(i, :);
    end
end

image_out(:, :, 1) = uint8(reshape(data(:, 1), row, column));
image_out(:, :, 2) = uint8(reshape(data(:, 2), row, column));
image_out(:, :, 3) = uint8(reshape(data(:, 3), row, column));
