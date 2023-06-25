% Data   X=dlmread('iris_label.txt');
% goi lenh [V3, U3, J3] = eSFCM(X, 3, 2, 0.01, 1000,U2,1);
function [V,U,J]=eSFCM(X,C,m,Eps,maxTest,U1,lamda)
%clc
[N,r]=size(X);
for i = 1:C
         for j = 1:r
            V(i,j) =  min(X(:,j))   + rand() *  (max(X(:,j)) - min(X(:,j)));
 % V(i,j) = randi(10);
 %            V(i,j) = min(X(:,j)); 
         end       
end


minU1=min(U1);
maxU1=max(U1);
for i=1:C
    for k=1:N
       if U1(i,k)==minU1(k)
           U1(i,k)=0;
       end
       if U1(i,k)==maxU1(k)
           U1(i,k)=U1(i,k)-minU1(k);
       end
    end
end

%lamda=2; 
%Tinh V ngang bang V1 tu U1
 for j = 1:C
           for i = 1:r
               tuso = 0;
               mauso = 0;
               for k = 1:N
                  mauso = mauso +  power(U1(j,k),2);
                  tuso = tuso + power(U1(j,k),2) * X(k,i);
               end
               if (mauso ~= 0) 
                   V1(j,i) = tuso / mauso;
               else
                   V1(j,i) = 0;
               end
           end
 end
% T�nh ma tr?n kho?ng c�ch D
%T�nh ma tr�n hi?p ph??ng sai C c?a Xi v� V1j l� ma tr?n P
    P=zeros(r,r);
    tong=0;
    for j=1:r
        for i=1:C
            for k=1:N
                tong=tong+power(U1(i,k),2)*(X(k,:)-V1(i,:))*(X(k,:)-V1(i,:))';

            end
        end

    P=tong/N;

    if det(P)~=0
        A=inv(P);
    else
        A=ones(r,r);
    end

%Vong lap
    dem = 0;
    while (1>0)
        for j = 1:C
            for k = 1:N
                tong1 = (X(k,:)-V(j,:))*A*(X(k,:)-V(j,:))';
                tong1=exp((-lamda)*tong1);
                %Tinh tong2
                tong2 = 0;
                for i = 1:C
                    tong2=tong2+U1(i,k);
                end    
                tong2=1-tong2;
                %Tinh tong3
                tong3=0;
                for i=1:C
                    tong4=(X(k,:)-V(i,:))*A*(X(k,:)-V(i,:))';
                    tong3=tong3+exp((-lamda)*tong4);
                end
                
                U(j,k) = U1(j,k)+(tong1*tong2)/tong3;
            end    
        end
         %chuan hoa U
         
        %Tinh V(t+1) tu U ra W
        for j = 1:C
           for i = 1:r
               tuso = 0;
               mauso = 0;
               for k = 1:N
                  mauso = mauso + U(j,k);
                  tuso = tuso + U(j,k) * X(k,i);
               end
               if (mauso ~= 0) 
                   W(j,i) = tuso / mauso;
               else
                   W(j,i) = 0;
               end
           end
        end   
        
        %So sanh V va W        
        saiso = 0;
        for i = 1:C
           for j = 1:r              
              saiso = saiso + power(W(i,j)-V(i,j),2); 
           end
        end
        saiso = sqrt(saiso);
        
        %Kiem tra sai so voi Eps
        if (saiso <= 0.5)
            break;
        else          
            %Lap tiep: Gan V = W
            for i = 1:C
                for j = 1:r
                    V(i,j)= W(i,j);
                end
            end
        end
        %Kiem tra voi so lan lap lon nhat
        if(dem>=maxTest)
            break;
        end
        %Tang so vong lap len
        dem = dem + 1;
   % saiso
    end

  J=0;
for k=1:N
    tong1=0;
    for j=1:C
        tong2=0;
        for i=1: r
            tong2=tong2+power(X(k,i)-V(j,i),2);
        end
        tong1=tong1+power(tong2,1-m);
    end
    J=J+power(tong1,1-m);
end



end