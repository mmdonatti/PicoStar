clear
clc
close all

files = {'NSLS_stair_0-50pA_1pA_10s.log';
           'NSLS_stair_0-10pA_500fA_5s.log';
           'NSLS_stair_0-5pA_100fA_5s.log';
           'LNLS_stair_0-50pA_1pA_10s.log';
           'LNLS_stair_0-10pA_500fA_5s.log';
           'LNLS_stair_0-5pA_100fA_5s.log';
           'NSLS_ShortTermDrift.log'};

for idx =1:length(files)    
    
    file_name = files{idx};
    file = fopen(file_name,'r');

    for i=1:31
        fgetl(file);
    end

    CH1 = [];
    CH2 = [];
    CH3 = [];
    CH4 = [];
    time_s = [];
    i = 1;
    while 1

        S = fgetl(file);
        if S == -1
            break
        end
        idx = strfind(S,'	');
        datestr = S(1:idx(1)-1);
        time_s(i) = 24*3600*datenum(datestr,'yyyy-mm-dd HH:MM:SS');
        CH1(i) = str2num(S(idx(2)+1:idx(3)-1));
        CH2(i) = str2num(S(idx(4)+1:idx(5)-1));
        CH3(i) = str2num(S(idx(6)+1:idx(7)-1));
        CH4(i) = str2num(S(idx(8)+1:end));

        i = i+1;
    end

    time_s(:) = time_s(:) - time_s(1); 

    figure
    plot(time_s,CH2,'LineWidth',2)
    grid on
    title([file_name],'Interpreter', 'none')
    ylabel('Current (pA)')
    xlabel('Time (s)')

    fclose(file);

end
% file_name = 'LNLS_stair_0-50pA_1pA_10s.log';
% file = fopen(file_name,'r');
% 
% for i=1:31
%     fgetl(file);
% end
% 
% CH1 = [];
% CH2 = [];
% CH3 = [];
% CH4 = [];
% time_s = [];
% i = 1;
% while 1
% 
%     S = fgetl(file);
%     if S == -1
%         break
%     end
%     idx = strfind(S,'	');
%     datestr = S(1:idx(1)-1);
%     time_s(i) = 24*3600*datenum(datestr,'yyyy-mm-dd HH:MM:SS');
%     CH1(i) = str2num(S(idx(2)+1:idx(3)-1));
%     CH2(i) = str2num(S(idx(4)+1:idx(5)-1));
%     CH3(i) = str2num(S(idx(6)+1:idx(7)-1));
%     CH4(i) = str2num(S(idx(8)+1:end));
% 
%     i = i+1;
% end
% 
% time_s(:) = time_s(:) - time_s(1); 
% 
% figure
% plot(time_s,CH2,'LineWidth',2)
% grid on
% title(['1 pA Step Curve - ',file_name],'Interpreter', 'none')
% ylabel('Current (pA)')
% xlabel('Time (s)')
% 
% fclose(file);
% 
% 
% file_name = 'ShortTermDrift.log';
% file = fopen(file_name,'r');
% 
% for i=1:31
%     fgetl(file);
% end
% 
% CH1 = [];
% CH2 = [];
% CH3 = [];
% CH4 = [];
% time_s = [];
% i = 1;
% while 1
% 
%     S = fgetl(file);
%     if S == -1
%         break
%     end
%     idx = strfind(S,'	');
%     datestr = S(1:idx(1)-1);
%     time_s(i) = 24*3600*datenum(datestr,'yyyy-mm-dd HH:MM:SS');
%     CH1(i) = str2num(S(idx(2)+1:idx(3)-1));
%     CH2(i) = str2num(S(idx(4)+1:idx(5)-1));
%     CH3(i) = str2num(S(idx(6)+1:idx(7)-1));
%     CH4(i) = str2num(S(idx(8)+1:end));
% 
%     i = i+1;
% end
% 
% time_s(:) = time_s(:) - time_s(1); 
% 
% figure
% plot(time_s,CH2,'LineWidth',1)
% grid on
% title(['Short Term Drift - ',file_name],'Interpreter', 'none')
% ylabel('Current (pA)')
% xlabel('Time (s)')
% y_lim = 2*max(abs(CH2));
% axis([0 time_s(end) -y_lim y_lim])
% fclose(file);
% 
% 
% 
