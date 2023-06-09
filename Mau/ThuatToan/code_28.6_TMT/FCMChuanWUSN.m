% Data   X=dlmread('sensors_data.txt');
% BS=[250 250 25]
% goi lenh [V,U1, J] = FCMChuanWUSN(X, 3, 2, 0.01, 1000, BS, 0.002, 20);
function [V,U,J]=FCMChuanWUSN(X,C,m,Eps,maxTest,BS, alpha, kU)
%clc
[N,r]=size(X);
efs = 10; % pJ/bit/m^2
emp = 0.0013;  
ground = 20;

%khoi tao random V
for i = 1:C
    for j = 1:r
        V(i,j) =  min(X(:,j))   + rand() *  (max(X(:,j)) - min(X(:,j)));
 % V(i,j) = randi(10);
 %            V(i,j) = min(X(:,j)); 
     end       
end
V_init = V
%Vong lap
dem = 0;
while (1>0)
    for i = 1:N
       for j = 1:C
          %Tinh tu so
          TuBS = 0;
          for k = 1:r
              TuBS = TuBS + power(V(j,k)-BS(1,k),2);
          end    
          TuBS = sqrt(TuBS);

          TuXi = 0;
          for k = 1:r
              TuXi = TuXi + power(X(i,k)-V(j,k),2);
          end
          TuXi = sqrt(TuXi);
          
          TuXiU = 0;
          if X(i, 3) < ground
              for k = 1:r
               TuXiU = TuXi + power(X(i,k)-V(j,k),2);
              end 
               TuXiU = sqrt(TuXi);
          end 
          
          Tu = emp * power(TuBS,4) + (N - C)*efs*power(TuXi, 2) + kU*((1/log(10)) + 8.69 * alpha)* TuXiU ;
          
          %Tinh mau so
           
          tong = 0;
          for l =1:C
              MauBS = 0;
              for k = 1:r
                  MauBS = MauBS + power(V(l,k)-BS(1,k),2);
              end    
              MauBS = sqrt(MauBS);
              
              MauXk = 0;
              for k = 1:r
                  MauXk = MauXk + power(X(i,k)-V(l,k),2);
              end    
              MauXk = sqrt(MauXk);
              
              MauXkU = 0;
              if(X(i, 3) < ground )
                  for k = 1:r
                      MauXkU = MauXkU + power(X(i,k)-V(l,k),2);
                  end    
                  MauXkU = sqrt(MauXkU);
              end 
              Mau = emp * power(MauBS,4) + (N - C)*efs*power(MauXk, 2) + kU*((1/log(10)) + 8.69 * alpha)* MauXkU ;
              
              tong = tong + power(Tu/Mau, 1/(m-1)); 
          end
        
          U(j,i) = 1/tong;  
       end    
    end
        %tinh khoang cach tongX(i) den BS)
        tongKC = 0;
        for i1 = 1:N
            tempKC = 0;
            for k1 = 1:r
                  tempKC = tempKC + power(X(i1,k1)-BS(1,k1),2);
            end    
            tongKC = tongKC + sqrt(tempKC);
        end
        
        %Tinh V(t+1) tu U ra W
        for j = 1:C
           tongU = 0;
           for k = 1:N
               tongU = tongU + power(U(j,k),m);
           end
           for t = 1:r
               
               %%%%theo Cardano chuan
%                a = 4*C* emp*tongU;
%                B = 2 * (N-C)*efs*tongU;
%                ct = -kU * (1/log(10) + 8.69*alpha)*tongU;
%                p = B/a;
%                q = (B*tongKCDenBS+ct)/a;
%                W1 = nthroot((-q/2)+ nthroot(power(q/2,2) + power(p/3,3),2),3) + nthroot((-q/2)- nthroot(power(q/2,2) + power(p/3,3),2),3)
%                W(j,i) = W1  + BS(1,i);
               
               %%%theo cong thuc tinh V trong bai cong thuc full
%                A = 4*C* emp*tongU;
%                B = 2 * (N-C)*efs*tongU;
%                ct = -kU * (1/log(10) + 8.69*alpha)*tongU;
%                W1 = (B/A)/nthroot(((B*tongKCDenBS + C)/2*A) + nthroot(0.25*power(((B*tongKCDenBS + C)/A),2) + power(B,3)/27*power(A,3),2) ,3);
%                W2 = nthroot(B/(2*A*tongKCDenBS + nthroot(0.25*power(((B*tongKCDenBS + C)/A),2) + power(B,3)/27*power(A,3),2)),3);
%                W(j,i) = W1 -W2 + BS(1,i);

               %%Theo cong thuc V rut gon
               mau2 = nthroot(0.25 * power((2*(N-C)*efs*tongKC - kU*(1/log(10) + 8.69*alpha))/4*C*emp ,2) + power(2*efs*(N-C),3)/27*power(4*C*emp,3),2);
               W1 = ((N-C)*efs/2*C*emp)/nthroot(((2*(N-C)*efs*tongKC - kU*(1/log(10) + 8.69*alpha))/8*C*emp) + mau2,3);
               W2 =  nthroot((2*(N-C)*efs*tongU)/(8*C*emp*tongU*tongKC + mau2),3);
               W(j,t) = W1-W2 + BS(1,t);
              
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
        if (saiso <= Eps)
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

MaxU=max(U);
for k=1:N
    for j=1:C
        if U(j,k)==MaxU(k)
            cum(k)=j;
        end
    end
end


end

function t = calcSumDistDataPoint2X(data, X)
temp = data - X(ones(size(data, 1), 1), :);
temp = temp.^2;
temp = sum(temp, 2);
temp = sqrt(temp);
t = sum(temp);
end


function PBM_value = PBM(numClust, data, center, U)
E_1 = calcSumDistDataPoint2X(data, mean(data));

maxU = max(U);
E_k = 0;
for i = 1 : numClust
    index = find(U(i,:) == maxU);
    clustData = data(index, :);
    E_k = E_k +  calcSumDistDataPoint2X(clustData, center(i, :));
end

D_k = 0;
for i = 1:numClust-1
    for j = i+1:numClust
        D_k = max(D_k, norm(center(i, :) - center(j, :)));
    end
end
    
PBM_value = (E_1 * D_k / (numClust * E_k)) ^ 2;
end


function SWC_value = SWC(numClust, data, U)
maxU = max(U);
SWC_value = 0;

wb = waitbar(0);
dem = 0;

for i = 1 : numClust
    index = find(U(i,:) == maxU);
    if size(index, 2) == 1
        continue;
    end
    clustData = data(index, :);
    for j = index
        a_i_j = calcSumDistDataPoint2X(clustData, data(j, :)) / size(index, 2);
        b_i_j = inf;
        for k = 1 : numClust
            if k ~= i
                index_k = find(U(k,:) == maxU);
                clustData_k = data(index_k, :);
                d_k_j = calcSumDistDataPoint2X(clustData_k, data(j, :)) / size(index_k, 2);
                b_i_j = min(b_i_j, d_k_j);
            end
        end
        SWC_value = SWC_value + (b_i_j - a_i_j) / max(a_i_j, b_i_j);
        dem = dem + 1;
        
%         waitbar(dem / size(data, 1), wb);
    end
end
SWC_value = SWC_value / size(data, 1);
end


        
function DB_value = DB(numClust, data, center, U)
    maxU = max(U);
    
    for i = 1 : numClust
        index = find(U(i,:) == maxU);
        clustData = data(index, :);
        stdData = std(clustData, 1);
        S(i) = sqrt(stdData(1)^2 + stdData(2)^2 + stdData(3)^2);
    end
    
    DB_value = 0;
    
    for i = 1:numClust
        maxSM = 0;
        for j = 1:numClust
           if j ~= i
               temp = (S(i) + S(j))/norm(center(i, :) - center(j, :));
               maxSM = max(maxSM, temp);
           end
        end
        DB_value = DB_value + maxSM;
    end
    
    DB_value = DB_value/numClust;
end

    
function IFV_value = IFV(numClust, data, sizeData, center, U)
    sigmaD = 0;
    sum = 0;
    
    for i = 1:numClust
        tg1 = 0;
        tg2 = 0;
        for j = 1:sizeData
            if U(j,i) == 0 
                U(j, i) = eps;
            end
            if U(j, i) == 1 
                U(j, i) = 1 - eps;
            end
            
            tg1 = tg1 + log(U(j, i))/log(2);
            tg2 = tg2 + U(j, i)^2;
            sigmaD = sigmaD + norm(data(j, :) - center(i, :))^2;
        end
        
        tg = (log(numClust)/log(2) - tg1/sizeData)^2;
        tg2 = tg2/sizeData;
        
        sum = sum + tg * tg2;
    end
    
    sigmaD = sigmaD/(numClust * sizeData);
    
    calcSDmax = 0;
    for i = 1:numClust-1
        for j = i+1:numClust
            calcSDmax = max(calcSDmax, norm(center(i, :) - center(j, :))^2);
        end
    end
    
    IFV_value  = (sum * calcSDmax) / (sigmaD * numClust);
end