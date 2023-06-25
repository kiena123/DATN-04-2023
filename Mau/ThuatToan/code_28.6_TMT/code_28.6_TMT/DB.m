function DB_value = DB(data, numClust, center, U)
    maxU = max(U);
    
    S = zeros(1, numClust);
    
    for i = 1 : numClust
        index = find(U(i,:) == maxU);
        
        for j = index
            S(i) = S(i) + norm(data(j, :) - center(i, :)) ^ 2;
        end
        S(i) = sqrt(S(i)/size(index, 2));
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