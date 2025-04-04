% -------------------------------------------------------------------------
% Generate aggregate uncertainty estimates
% -------------------------------------------------------------------------
cd('D:\files\uncertainty\mec_test2\mec_test2')
% Initialization

clear; clc;
load country; 
load ut;
[T,N,h] = size(ut);

% Cross-sectional average
utcsa = squeeze(mean(sqrt(ut),2));

% Principal component analysis
utpca = zeros(T,h);
for j = 1:h
   logu    = log(sqrt(ut(:,:,j)));
   dlogu(:,:,j)  = logu(2:end,:) - logu(1:end-1,:);
   [de,du,dl,dv] = factors(dlogu(:,:,j),3,2,1);
   % Rotate estimate
   rho     = corr(cumsum([0;du(:,1)]),utcsa(:,j));
   if rho < 0; 
       du  = -du; 
       dl  = -dl; 
   end;
   ufac    = cumsum([zeros(1,size(du,2));du]);
   dufac(:,:,j) = du;
   dlam(:,:,j)  = dl;
   deig(:,j)  = dv;
   % Calibrate to cross-section mean
   sd      = std(utcsa(:,j));
   mn      = mean(utcsa(:,j));
   p0      = [1,0.5];
   opt     = optimset('tolfun',1e-50,'display','off');
   [p,obj] = fminsearch(@(p)calibratef(p,ufac(:,1),sd,mn),p0,opt);
   utpca(:,j) = exp((p(1)*ufac(:,1)+p(2))./2); 
end
% 保存为Excel文件（新增部分）
%writematrix(utcsa, 'utcsa.xlsx');    % 保存为根目录下的utcsa.xlsx
% writematrix(utcsa, 'D:\files\uncertainty\mec_test2\mec_test2\output（对齐）\加拿大\utcsa.xlsx');  
% writematrix(dates, 'D:\files\uncertainty\mec_test2\mec_test2\output（对齐）\加拿大\dates.xlsx');   
% writematrix(utpca, 'D:\files\uncertainty\mec_test2\mec_test2\output（对齐）\加拿大\utpca.xlsx');
folder = fullfile('D:', 'files', 'uncertainty', 'mec_test2', 'mec_test2', 'output（对齐）', country);
file_path = fullfile(folder, 'utcsa.xlsx');
writematrix(utcsa, file_path);  
file_path = fullfile(folder, 'dates.xlsx');
writematrix(dates, file_path);   
file_path = fullfile(folder, 'utpca.xlsx');
writematrix(utpca, file_path);    % 保存为根目录下的utpca.xlsx
% Save results
save aggu dates ut utpca utcsa dufac dlam deig dlogu






