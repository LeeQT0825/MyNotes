# select

# poll

# epoll
## 概述
&emsp;*epoll*是Linux特有的*I/O*复用函数，其实现和*select*、*poll*有很大区别。*epoll*将用户关心的文件描述符上的事件放在内核里的一个事件表中，从而无须像*select*和*poll*那样每次调用都要重复传入文件描述符集或事件集，但是*epoll*需要一个额外的文件描述符来标识内核中的这个事件表。与*poll*不同的是，*epoll*如果检测到事件，就将所有就绪时间从内核时间表中复制到*events*指向的数组中，这样就极大提高了应用程序检索就绪文件描述符的效率，从 $O(n)$ 的时间复杂度降为了 $O(1)$ 。

## 函数
```cpp
#include<sys/epoll.h>
// 内核中创建事件注册表，返回注册表描述符epfd
int epoll_create(int size); 
// 对注册表进行操作，op为操作数，fd为待注册的描述符，event为事件结构体    
int epoll_ctl(int epfd, int op, int fd, struct epoll_event* event);
// 等待就绪事件并返回就绪事件的个数（-1为erron），events为就绪事件的数组（事件就绪后放入这里）     
int epoll_wait(int epfd, struct epoll_event* events, int maxevents，int timeout);       
```
## epoll对于文件描述符的操作有两种模式：LT和ET
### LT
&emsp;LT是默认模式，这种模式下其效率相当于一个稍微改进的*poll*，效率没有显著提高。
&emsp;对于LT模式的文件描述符，当*epoll_wait*检测到其上有事件发生并将此事件通知应用程序后，因公程序可以不立即处理该事件，这样当*epoll_wait*再次被触发，还会再向应用程序通告此事件，知道该事件被处理。
* 代码
    ```cpp
    void lt(epoll_event* events, int number, int epollfd, int listenfd) {
        char buf[BUFFER_SIZE];
        for (int i = 0; i < number; i++) {
            int sockfd = events[i].data.fd;
            //如果注册表中第i个socket还未与客户端建立连接（仍处于listen状态），则与客户端建立连接，并将两种模式加入到注册表中
            if (sockfd == listenfd) {       
                struct sockaddr_in client_address;
                socklen_t client_addrlength = sizeof(client_address);
                int connfd = accept(listenfd, (struct sockaddr*)&client_address, &client_addrlength);
                printf("listenfd converted\n");
                addfd(epollfd, connfd, false);
            }
            else if (events[i].events & EPOLLIN) {      //检查是否是默认工作模式
                printf("event trigger once\n");
                memset(buf, 0, sizeof(buf));
                int ret = recv(sockfd, buf, BUFFER_SIZE, 0);
                if (ret <= 0) {
                    close(sockfd);
                    continue;
                }
                printf("get %d bytes of content: %s\n", ret, buf);
            }
            else printf("something else happened\n");
        }
    }
    ```
* 输出
    ```cpp
    epoll_wait size: 1
    listenfd converted
    epoll_wait size: 1
    event trigger once
    get 10 bytes of content: asdghfdjah
    epoll_wait size: 1
    event trigger once
    get 10 bytes of content: gfkjhgkshd
    epoll_wait size: 1
    event trigger once
    get 10 bytes of content: fkjhasgdsf
    epoll_wait size: 1
    event trigger once
    get 2 bytes of content: 
    ```

### ET
&emsp;当*epoll_wait*检测到其上有事件发生，将其通告应用程序，应用程序必须马上处理，因为后续的*epoll_wait*将不再向应用程序通知这一事件。可见，ET模式降低了同一个*epoll*事件被重复触发的次数，所以效率更高。
* 代码
    ```cpp
    void et(epoll_event* events, int number, int epollfd, int listenfd) {
        char buf[BUFFER_SIZE];
        for (int i = 0; i < number; i++) {
            int sockfd = events[i].data.fd;
            if (sockfd == listenfd) {
                struct sockaddr_in client_address;
                socklen_t client_addrlength = sizeof(client_address);
                int connfd = accept(listenfd, (struct sockaddr*)&client_address, &client_addrlength);
                addfd(epollfd, connfd, true);       //将在revents[]中的listenfd都与客户端链接，并向事件注册表中添加已连接的fd
            }
            else if (events[i].events & EPOLLIN) {
                //这段代码不会被重复触发，所以我们循环读取
                printf("event trigger once\n");
                while (1) {
                    memset(buf, 0, sizeof(buf));
                    int ret = recv(sockfd, buf, BUFFER_SIZE, 0);
                    if (ret < 0) {
                        //非阻塞模式的I/O，当下面的条件成立表示数据已经全部取走
                        if ((errno == EAGAIN) || (errno == EWOULDBLOCK)) {
                            printf("read later\n");
                            break;
                        }
                        close(sockfd);
                        break;
                    }
                    else if (ret == 0) close(sockfd);
                    else printf("get %d bytes of content: %s\n", ret, buf);
                }
            }
            else printf("something else happened\n");
            printf("epoll_wait done\n");
        }
    }
    ```
* 输出
  ```cpp
    epoll_wait size: 1
    epoll_wait done
    epoll_wait size: 1
    event trigger once
    get 10 bytes of content: dsadxgfcxh
    get 10 bytes of content: gfchgfhgfc
    get 10 bytes of content: hgfcgfcg


    read later
    epoll_wait done
  ```

### 总结
&emsp;在上面的实验中，同样发送*25*个字符，第一个LT工作模式下*epoll*一共向应用程序通知了三次，而第二种的ET工作模式仅仅通知一次。