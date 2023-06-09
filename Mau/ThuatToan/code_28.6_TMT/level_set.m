%X=dlmread('img_1')
%level_set
function Img_corrected=level_set(Img)
% close all;
% clear all;
% Img=imread('img_1.jpg');
Img=double(Img(:,:,1));
A=255;
Img=A*normalize01(Img); % rescale the image intensities
nu=0.001*A^2; % coefficient of arc length term

sigma = 8; % scale parameter that specifies the size of the neighborhood
iter_outer=50; 
iter_inner=10;   % inner iteration for level set evolution

timestep=.1;
mu=2;  % coefficient for distance regularization term (regularize the level set function)

c0=1;
%figure(1);
imagesc(Img,[0, 255]); colormap(gray); axis off; axis equal

% initialize level set function
initialLSF = c0*ones(size(Img));
initialLSF(30:90,50:90) = -c0;
u=initialLSF;

hold on;
contour(u,[0 0],'r');
title('Initial contour');

%figure(2);
imagesc(Img,[0, 255]); colormap(gray); axis off; axis equal
hold on;
contour(u,[0 0],'r');
title('Initial contour');

epsilon=1;
b=ones(size(Img)); 

K=fspecial('gaussian',round(2*sigma)*2+1,sigma); 
KI=conv2(Img,K,'same');
KONE=conv2(ones(size(Img)),K,'same');

[row,col]=size(Img);
N=row*col;

for n=1:iter_outer
    [u, b, C]= lse_bfe(u,Img, b, K,KONE, nu,timestep,mu,epsilon, iter_inner);

    if mod(n,2)==0
        %pause(0.001);
        imagesc(Img,[0, 255]); colormap(gray); axis off; axis equal;
        hold on;
        contour(u,[0 0],'r');
        iterNum=[num2str(n), ' iterations'];
        title(iterNum);
        hold off;
    end
   
end
Mask =(Img>10);
Img_corrected=normalize01(Mask.*Img./(b+(b==0)))*255;

%figure(3); imagesc(b);  colormap(gray); axis off; axis equal;
%title('Bias field');

% figure(1);
imagesc(Img_corrected); colormap(gray); axis off; axis equal;
title('Bias corrected image');
end
