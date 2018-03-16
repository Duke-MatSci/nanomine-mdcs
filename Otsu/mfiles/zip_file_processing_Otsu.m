function zip_file_processing_Otsu(path_to_write)

    path_to_unzip_files = [path_to_write,'/input'];

    images = dir([path_to_unzip_files]);

    num_images = length(images)-2;

    for i = 1 : num_images
        img = imread([path_to_unzip_files,'/',images(i+2).name]);
        imwrite(img,[path_to_write,'/','Input',num2str(i),'.jpg']);
        if length(size(img)) > 2
           img = img(:,:,1);
        end
        Target = double(img);
        Target = Target/256; % convert to grayscale
        % Otsu Method
        level = graythresh(Target);
        Target_binarized = im2bw(Target,level);
        %Save binarized image
        imwrite(Target_binarized,[path_to_write,'/','Binarized_Input',num2str(i),'.jpg']);
    end
end
