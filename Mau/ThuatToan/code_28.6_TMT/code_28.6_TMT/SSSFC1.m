% Data   X=dlmread('iris_label.txt');
% goi lenh [V,U, J] = SSSFC1(X, 3, 2, 0.01, 1000,U1);
function [V,U,J]=SSSFC1(X,C,m,Eps,maxTest)
clc
[N,r]=size(X);
for i = 1:C
         for j = 1:r
            V(i,j) =  min(X(:,j))   + rand() *  (max(X(:,j)) - min(X(:,j)));
 % V(i,j) = randi(10);
 %            V(i,j) = min(X(:,j)); 
         end       
end

for i = 1:N
       for j = 1:C
          %Tinh tu so
          Tu = 0;
          for k = 1:r
              Tu = Tu + power(X(i,k)-V(j,k),2);
          end    
          Tu = sqrt(Tu);

          %Tinh mau so
           
          tong = 0;
          for l =1:C
              Mau = 0;
              for k = 1:r
                  Mau = Mau + power(X(i,k)-V(l,k),2);
              end    
              Mau = sqrt(Mau);
              tong = tong + power(Tu/Mau, 2/(m-1)); 
          end
        
          U1(j,i) = 1/tong;  
       end    
end
    %Vong lap
dem = 0;
while (1>0)
  if m>1
     for j = 1:C
       for i = 1:N
          %Tinh tong1
          tong1 = 0;
          for k = 1:C
              tong1=tong1+U1(k,i);
          end    
          tong1=1-tong1;
          %Tinh tong2
           
          d1 = 0;
          for k =1:r
              d1 = d1 + power(X(i,k)-V(j,k),2);
          end    
          
          %tong2 = sqrt(tong2);
          %Tinh tong3
          tong3=0;
          for k=1:C
              d2=0;
              for l=1:r
                  d2 = d2 + power(X(i,l)-V(k,l),2);
              end
              
              tong3=tong3+power(1/d2,1/(m-1));
          end
            
          U(j,i) = U1(j,i)+tong1*power(1/d1,1/(m-1))/tong3;
       end    
     end
     
    else
         for j = 1:C
           for i = 1:N
              
               for k=1:C
                   d2(k)=0;
                  for l=1:r
                      d2(k) = d2(k) + power(X(i,l)-V(k,l),2);
                  end
              end
              mink=min(d2)
              if j==mink
                  tong1=0;
                  for k=1:C
                      tong1=tong1+U1(k,i);
                  end
                  U(j,i)=U1(j,i)+1-tong1;
              else
                  U(j,i)=U1(j,i);
              end
           end
         end
    end
                       
        %Tinh V(t+1) tu U ra W
        for j = 1:C
           for i = 1:r
               tuso = 0;
               mauso = 0;
               for k = 1:N
                  mauso = mauso + power(abs(U(j,k)-U1(j,k)),m);
                  tuso = tuso + power(abs(U(j,k)-U1(j,k)),m) * X(k,i);
               end
               if (mauso ~= 0) 
                   W(j,i) = tuso / mauso;
               else
                   W(j,i) = 0;
               end
           end
        end   
        
        %So sanh W va V        
        saiso = 0;
        for i = 1:C
           for j = 1:r              
              saiso = saiso + power(W(i,j)-V(i,j),2); 
           end
        end
        saiso = sqrt(saiso);
        
        %Kiem tra sai so voi Eps
        if (saiso <= 0.00000001)
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
    
% U
% sum(U)
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
MaxU=max(U);
for k=1:N
    for j=1:C
        if U(j,k)==MaxU(k)
            cum(k)=j;
        end
    end
end

end