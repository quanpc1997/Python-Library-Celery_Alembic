# Celery

## A. Lý thuyết
### 1. Celery là gì?
- **Celery là một task queue giúp quản lý và khởi chạy các task dưới background trong một hệ thống phân tán**. Nó là một công cụ mạnh mẽ để cải thiện hiệu năng của hệ thống phân tán bằng cách chạy các task bất đồng bộ. 

- Nó hoạt động bằng cách gửi các messages giữa Django applications và các worker thông qua một broker như là RabbitMQ hoặc Redis. 

- Tác dụng chính của Celery là cho phép chúng ta giảm tải các tasks yêu cầu time chạy lâu từ app chính và lên cho các tác vụ chạy theo yêu cầu hoặc ttheo khoảng thời gian đều đặn. Nó cũng cung cấp các tùy chọn để  ưu tiên các nhiệm vụ và quản lý tài nguyên hiều quả. 

### 2. Kiến trúc của Celery.
Kiến trúc của Celery bao gồm các thành phần sau:

![The architecture of Celery](./images/1-architecture_of_celery.png)

1. **Task producers**: Là thành phần tạo ra các task và submit chúng đến task queue. Chúng có thể là Django views, command-line scripts, hoặc bất kì code nào để chạy một task bất đồng bộ.
2. **Message broker**: Đây là một message queue service có trách nhiệm là lưu trữ các task cho đến khi chúng sẵn sàng được xử lý. Một vài message brokers phổ biến bao gồm RabbitMQ và Redis [Xem thêm](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html).
3. **Worker/Task consumers**: Đây là thành phần lắng nghe xem task nào đang ở đầu của hành đợi để thực hiện chúng. Có thể có nhiều worker chạy trong các máy tính khác nhau.
4. **Result backend**: Đây có thể là 1 loại hệ quản trị cơ sở dữ liệu hoặc là một message queue được sử dụng để lưu trữ kết quả của tasks. Thành phần này là một optional, nhưng nó có thể thường được sử dụng để  truy xuất kết quả của tasks sau khi worker thực hiện chúng.

- Kiến trúc này cho phép mở rộng theo chiều ngang bằng cách thêm nhiều hơn các worker/task consumers để xử lý được nhiều công việc hơn.


Celery sẽ chạy theo những bước sau:
1. Task Producers sẽ tạo ra các task và submit nó đến các message broker. 
2. Các worker sẽ lắng nghe các tasks trong message queue và thực hiện chúng. Kết quả của các task được lưu vào backend nếu chúng ta configure.

### 3. Tại sao chúng ta sử dụng Celery.
Có một vài lý do sau để ta thường sử dụng đến Celery:
1. **Giảm tải các task vụ cần nhiều time để xử lý**: Nếu bạn có nhiều task cần tốn nhiều time để chạy. Bạn có thể sử dụng Celery để chạy chúng trong background trong khi người dùng có thể tiếp tục sử dụng ứng dụng web của bạn. 
2. **Gửi emails**: Đây là một tác vụ phổ biến thường được dùng với celery để tối ưu time khi việc gửi mail sẽ được thực hiện bất đồng bộ.
3. **Chạy các task định kì**: Nếu bạn có các task chạy đình kì một cách thường xuyên, như là lấy dữ liệu từ một website hoặc gửi các báo cáo đinh kì, thì bạn có thể sử dụng Celery để lên lịch cho nó.
4. **Xử lý trong hệ thống phân tán**: Nếu bạn có một lượng lớn dữ liệu cần được xử lý, bạn có thể sử dụng Celery để chia các task vào các workers để làm giảm thời gian xử lý.
5. **Đinh tuyến tác vụ**: Nếu bạn có các task cần định tuyến chúng đến các queues khác nhau (dựa vào kiểu của task hoặc độ ưu tiên của task) tính năng định tuyến của Celery sẽ làm điều này.

### 4. Tại sao chúng ta lại dùng Celery thay vì multithreading, async hay multiprocessing?
Đa luồng, không đồng bộ và đa xử lý đều là các tùy chọn để thực thi mã đồng thời trong Python và chúng có thể hữu ích trong một số trường hợp nhất định. Tuy nhiên, chúng có thể không phải lúc nào cũng là lựa chọn tốt nhất để thực thi các tác vụ không đồng bộ trong môi trường phân tán.

Celery được thiết kế đặc biệt để hỗ trợ thực thi tác vụ phân tán và nó cung cấp một số tính năng có thể hữu ích trong ngữ cảnh này. Ví dụ: Celery có thể tự động thử lại các tác vụ không thành công do worker thực hiện task đó gặp sự cố hoặc các sự cố khác và có thể định tuyến các tác vụ đến các hàng đợi khác nhau dựa trên loại tác vụ hoặc mức độ ưu tiên của tác vụ. Ngoài ra, Celery sử dụng tính năng truyền message để giao tiếp giữa các worker và message queue, điều này có thể hữu ích nếu bạn cần truyền một lượng lớn dữ liệu giữa các tác vụ hoặc nếu bạn muốn tách riêng việc thực thi các tác vụ khỏi phần còn lại của ứng dụng.

Nhìn chung, mặc dù đa luồng, không đồng bộ và đa xử lý có thể đủ cho một số loại thực thi đồng thời nhất định, nhưng Celery cung cấp giải pháp mạnh mẽ và giàu tính năng hơn để thực thi các tác vụ không đồng bộ trong môi trường phân tán. Có một vài lý do tại sao chúng tôi có thể chọn sử dụng Celery thay vì các tùy chọn đồng thời khác, chẳng hạn như đa luồng, không đồng bộ hoặc đa xử lý:
- **Thực thi phân tán**: Celery được thiết kế để xử lý các tác vụ phân tán. Điều này có nghĩa là bạn có thể nâng cao hiệu suất bằng cách thêm nhiều hơn các worker, điều này có thể hữu ích nếu bạn có một số lượng lớn tác vụ cần xử lý hoặc nếu tác vụ của bạn cần nhiều tính toán.
- **Lên lịch cho tác vụ**: Celery cung cấp tính năng lên lịch để thực thi các task trong một khoảng time xác định hoặc là các task được chạy định kỳ.
- **Khả năng chịu lỗi**: Celery sử dụng messages để giao tiếp giữa worker và Message queue. Điều này hữu dụng nếu bạn cần đưa một lượng lớn dữ liệu qua các task hoặc nếu bạn muốn tách rời phần thực thi task với phần còn lại của app.

### 5. Những điểm hạn chế của celery.
1. **Phức tạp**: Celery là một thư viện nhiều tính năng có thể xây dựng được các hệ thống phức tạp và mạnh mẽ, nhưng nhược điểm là khó cài đặt và nó yêu cầu một message broker và đó có thể là một thách thức để quản lý và cấu hình trong môi trường product.
2. **Độ trễ**: Celery sử dụng các message để giao tiếp giữa các task producers và các worker, điều này có thể sản sinh ra độ trễ trong hệ thống. Độ trễ có thể được giảm đi bằng các sử dụng một fast message broker và tối ưu lại cấu hình, nhưng nó sẽ yêu cầu phải một kỹ sư phải thật am hiểu.
3. **Debugging**: Đây cũng là một thách thức, như là các task execution và main applicaion đang chạy trong các worker khác nhau. Điều này có thể làm cho ta khó trong việc tìm ra luồng kiểm soát và xác định lỗi.
4. **Khả năng mở rộng**: Celery được thiết kế để mở rộng theo chiều ngang bằng cách thêm nhiều worker, nhưng nó có thể là thách thức khi mở rộng theo chiều dọc bởi việc tăng tài nguyên cho từng máy tính. 
5. **Bảo mật**: Nếu cấu hình không đúng, Celery có thể dễ bị tấn công như là DOS và message injection.
6. **Kém hỗ trợ cho window**: Mặc dù có thể chạy trên hệ điều hành windows, nhưng nó được hỗ trợ giới hạn và việc cài đặt và cấu hình rất khó khăn.

## B. Thực hành
<p style="color:red">Cần cài và dựng thành công 1 cluster lên và hoàn thành nốt nội dung này</p>

## C. Tham khảo
https://www.geeksforgeeks.org/celery-integration-with-django/

https://www.linode.com/docs/guides/task-queue-celery-rabbitmq/

