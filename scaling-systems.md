# Scaling Systems
When designing systems, one of the biggest questions is around scaling: How do I scale my system to handle an ever increasing amount of data and calls to my service? There are three potential solutions:
1. Scale vertically 
2. Shard your database 
3. Scale horizontally 

## Scale Vertically
Scaling vertically means adding more resources to your current box: add more memory, add more hard disk space, etc. Rather than trying to add more machines, you first find a way to make your existing monolithic system work. At the beginning, scaling vertically is almost always the easier and simplest solution, because distributed systems come with additional overhead (discussed in more detail below).

Aside from adding more CPU and more memory, you can also scale your existing database by investingating whether your data should be denormalized (if joining is the bottleneck in your query performance) and whether your data should be migrated to a NoSQL database (e.g. MongoDB), which typically, but not always, scales better than a traditional relational database.

## Shard Your Database 
If your database is too large to fit on one box, you might consider sharding your database. Sharding means splitting the data across multiple machines in a logical way such that your service can quickly figure out which data is on which machine. For example, if virtually all queries only ever retrieve profile data for one customer at a time, you might shard your data based on customer ID.

Another option is to shard your database vertically, in which you partition your data by feature. For example, you might have one partition for all profile data, another partition for posts, and another partition for photos. In either case, sharding splits up your database to make it more manageable to handle, provided you shard in such a way that you rarely have to query across shards. 

## Scale Horizontally
### Master-Slave Setup 
Aside from scaling vertically and sharding your database, you can also scale out. When you think about the largest services in the world (e.g. Google, Facebook), the throughput for reads differs significantly from writes. For example, Google's search engine is hit by millions of read requests every second--whereas reindexing happens much less frequently. Hence, there is an opportunity to distribute reads vs. writes so that your service can scale up for each part independently.

This is typically achieved through a master-slave system. The single master box receives all write requests, whereas multiple slave boxes receive all read requests. Such a setup causes "slave lag", because the data replicated on the slave boxes takes time to catch up to the master's latest writes.

This single master-multiple slave setup works well for systems that require __high availability__, such as the read-heavy databases mentioned above. In such a system, you can readily scale up your read slave boxes (or add more slaves) to handle increased read throughput, without paying more for your write box. Hence, this distributed setup can be more cost-efficient.

In addition, scaling out can make your system more resilient. Since you now have multiple slaves handling read requests, if one goes down, the other slaves can still serve read requests. This is in contrast to sharding, in which if one database goes down, all the data on that shard is no longer accessible.

Of course, distributed systems come with their own overhead and complexities, which make them far more difficult to manage than scaling up or sharding your database. These will be discussed later on.

### Availability vs. Consistency 
The above master-slave system functions well for read-heavy systems--that is, systems that require highly  available data, at the cost of having slightly outdated data (due to "slave lag").

However, you can imagine that some services require high consistency rather than high availability. For example, a bank system likely wants any read request to retrieve the same, correct result every time. Otherwise, a customer might withdraw more than is available in their account. Hence, consistency is extremely important, even at the cost of slowing down read requests, or making the read unavailable while the system is syncing up between boxes.

Such systems utilize Paxos, a family of protocols for ensuring consensus amongst all boxes. This typically involves exchanging a series of promises between slaves and master(s) to determine who has the latest version of the data--before this latest version is propagated across all boxes.

Hence, we have arrived at the well-known __CAP theorem__, which states the following:
1. Network failure is inevitable; hence, data will not always transfer successfully between machines 
2. In the presence of network failure, a system can either be highly available, or highly consistent, but not both 

Your final choice of master-slave setup will depend on this tradeoff between availability and consistency.

### Issues with Distributed Systems 
Despite the benefits of distributed systems, they come with increased overhead and complexity in coordinating between boxes.

_Slave Failure_<br> 
First, what happens if a slave fails? Naively, you may think that this is easy to handle since you have additional slaves to serve reads. However, imagine that your service handles a billion calls a second, split up between two slave boxes. Now, if your first slave box goes down, your second slave box is hit with double the amount of queries that it normally handles. Consequently, _that_ doubled load then causes the second box to go down.  Hence, you need to have at least three boxes to ensure that the remaining boxes can continue serving the increased traffic.

In addition, to boot up a new slave (replacing the failed slave), you ideally boot this up from a backup. That is, for large databases, it would take far too long to read through the entire write log and run all those updates. Instead, every night, you run backups off your database and offload the tar file to S3. This way, you can quickly restart a new box off of that snapshot, then apply the latest writes over the past few hours. 

_Master Failure_<br>
Secondly, what happens if a master fails? One solution is to always have a separate parallel cluster running, allowing you to quickly switch over to the parallel system in the case of master failure. However, this solution could become prohibitively costly for the largest systems. 

Another solution is to promote one of your slaves to become the master. While this may sound simple, you quickly run into issues with network communication failures. For example, say you have three slave boxes when the master goes down. The slave boxes now "vote" to determine who should become the new master.

Unfortunately, one of your slave boxes cannot communicate with the other two slaves. It casts a vote for itself to become master, and since it receives no votes against (due to network issues), it now promotes itself to master. Similarly, the other two boxes vote amongst themselves and promote another master--and now you have two masters running your system. 

This is known as the __leader election__ problem, in which you must design a fail-safe algorithm for promoting exactly one slave to become the master. 

### Microservices 
Distributed systems relate to microservices, which have risen in popularity over the last few years. Rather than colocating all services in one monolithic system, many companies opt to split out their features into numerous microservices across multiple boxes. For example, a system like Facebook might have one microservice for account logins, one for authentication, another for newsfeed, and another for Messenger (obviously for a system at the scale of Facebook, these would be broken down even further).

Microservice architecture has several benefits:
1. Each service can be scaled independently: If newsfeed is the most popular feature today, scale that service up (without incurring costs for the account microservice)
2. Each feature can be deployed separately: If the Messenger teams wants to deploy a new photo sharing feature, they do not have to take down the entire system, which might happen in a monolithic system 

Again, there are tradeoffs with having to coordinate between these microservices. This setup may also make it harder to release features that span multiple services. All of these should be considered in designing the architecture for your system.