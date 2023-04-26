% Data X=dlmread('iris_label.txt');
%Chay [V,U,J]=SSFCMBP(X,3,2,0.01,150,U1);
function [V,U,J]=SSFCMBP(X,C,m,Eps,maxTest,U1)
%clc;
%X=dlmread('iris_label.txt');
%C=input('so cum la=');
%m=input('so mo hoa=');
%Eps=input('nhap Eps=');
%t=input('nhap To=');
%beta=input('nhap so beta=');
%maxTest=input('nhap so lan lap lon nhat=');
%H=input('nhap so luong nhan=');

[N,r]=size(X);
%Kh?i t?o t�m ban ??u ng?u nhi�n
for i = 1:C
         for j = 1:r
            V(i,j) =  min(X(:,j))   + rand() *  (max(X(:,j)) - min(X(:,j)));
 % V(i,j) = randi(10);
 %            V(i,j) = min(X(:,j)); 
         end       
end
     
% minU1=min(U1);
%for i=1:C
 %   for k=1:N
  %     if U1(i,k)==minU1(k)
   %        U1(i,k)=0;
   %    else
    %       U1(i,k)=0;
    %   end
   % end
%end

%Gan nhan thu cong
L=zeros(N,1);
H=2;
MaxU1=max(U1);
for k=1:N
    for j=1:C
        if U1(j,k)==MaxU1(k)
             L(k)=j;
        end
    end
end

%Tinh B chinh la xich ma trong cong thuc
B=ones(N,1);

beta=0.06;
%Tao lop ngau nhien
dem=0;
for k=1:N
     if L(k)==1   
        H1(k)=1;
     else
         H1(k)=2;
     end
     dem=dem+1;
end
Alpha=dem/N;
%Tinh F
for i=1:H
    for k=1:N
        if H1(k)==i
            F(i,k)=1;
        else
            F(i,k)=0;
        end
    end
end

Pi=zeros(H,C);
for i=1:H
    for j=1:C
        for k=1:N
            if (H1(k)==i) & (L(k)==j)
                Pi(i,j)=j;
            end
            
        end
    end
end


%Xac dinh ma tran M
for i=1:H
    for j=1:C
        if Pi(i,j)==j
            M(i,j)=1;
        else
            M(i,j)=0;
        end
    end
end
demM=0;
while (1>0)
demU1=0;
    while (1>0)
        %Tinh U11 ch�nh l� U1 theo ct (24)
        for i=1:C
            for k=1:N
                tong1=0;
                for j=1:H
                    tong2=0;
                    
                    for s=1:C
                        if (Pi(j,s)==s)
                                tong2=tong2+U1(s,k);
                         end
                    end
                    ok=false;
                    for s=1:C
                        if Pi(j,s)==L(k)
                            ok=true;
                        end
                    end
                    if ok
                        tong1=tong1+(F(j,k)-tong2);
                    end
                                    
                end
                   U11(i,k)=U1(i,k)+2*beta*B(k)*tong1;
            end
        end
       saiso = 0;
        for i = 1:C
           for j = 1:N              
             saiso = saiso + power(U11(i,j)-U1(i,j),2); 
           end
        end
        saiso = sqrt(saiso);
   %Kiem tra sai so voi Eps
        if (saiso <= 0.01)
            break;
        else          
            %Lap tiep: Gan U1 = U11
            for i = 1:C
                for j = 1:N
                    U1(i,j)= U11(i,j);
                end
            end
        end
        %Kiem tra voi so lan lap lon nhat
        if(demU1>=maxTest)
            break;
        end
        %Tang so vong lap len
       demU1 = demU1 + 1;
    end
demU1;

%Tinh U theo ct (23)
demV=0;
while (1>0)
    for k = 1:N
           for j = 1:C
              %Tinh tu so
              D(k,j) = 0;
              for i = 1:r
                  D(k,j) = D(k,j) + power(X(k,i)-V(j,i),2);
              end    
              D(k,j) = sqrt(D(k,j));
           end
    end

    for i=1:C
        for k=1:N
            Tu=0;
            Mau=0;
            for l=1:C
                Tu=Tu+U11(l,k);
                Mau=Mau+power(D(k,i),1)/power(D(k,l),1);
            end
            U(i,k)=(Alpha*U1(i,k))/(1+Alpha)+(1-Alpha*Tu/(1+Alpha))/Mau;
        end
    end
  
      
    %chuan hoa U tr�nh sai s? t�ch l?y
    maxU=max(U);
    for i=1:C
        for k=1:N
            if U(i,k)==maxU(k)
                tong1=0;
                for j=1:C
                    tong1=tong1+U(j,k);
                end
                U(i,k)=1-tong1+U(i,k);
            end
        end
    end
    
%T�nh W theo ct (25), ch�nh l� V
    for i=1:C
        for j=1:r
            Tu=0;
            Mau=0;
            for k=1:N
                Tu=Tu+(power(U(i,k),2)+Alpha*power(U(i,k)-U11(i,k),2))*X(k,j);
                Mau=Mau+power(U(i,k),2)+Alpha*power(U(i,k)-U11(i,k),2);
            end
            W(i,j)=Tu/Mau;
        end
    end
    saiso = 0;
        for i = 1:C
           for j = 1:r              
             saiso = saiso + power(W(i,j)-V(i,j),2); 
           end
        end
        saiso = sqrt(saiso);
   %Kiem tra sai so voi To
        if (saiso <= 0.0001)
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
        if(demV>=maxTest)
            break;
        end
        %Tang so vong lap len
       demV = demV + 1;
end

%Tinh lai M
MaxU=max(U);
for k=1:N
    for j=1:C
        if U1(j,k)==MaxU(k)
             L(k)=j;
        end
    end
end
for i=1:H
    for j=1:C
        for k=1:N
            if (H1(k)==i) & (L(k)==j)
                Pi(i,j)=j;
            end
            
        end
    end
end
for i=1:H
    for j=1:C
        if Pi(i,j)==j
            M1(i,j)=1;
        else
            M1(i,j)=0;
        end
    end
end
if M==M1
    break;
end
if(demM>=maxTest)
            break;
end
        demM=demM+1;
end

%Tinh Lamda theo ct(22)
Tu=0;
Mau=0;
for i=1:C
    for k=1:N
        Tu=Tu+U1(i,k);
        Mau=Mau+1/(2*(1+Alpha)*power(D(k,i),2));
    end
end
Lamda=(1-(Alpha*Tu)/(1+Alpha))/Mau;

%T�nh h�m m?c ti�u J
J=0;
tong1=0;
tong2=0;
tong3=0;
for i=1:C
    for k=1:C
        tong1=tong1+power(U(i,k),2)*power(D(k,i),2);
        tong2=tong2+power(U(i,k)-U1(i,k),2)*power(D(k,i),2)*B(k);
        tong3=tong3+U(i,k);
    end
end
J=tong1+Alpha*tong2-Lamda*(tong3-1);

end

