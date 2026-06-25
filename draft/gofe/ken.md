### Transcript

Good afternoon everyone and welcome to the robotics seminar. It's a pleasure
and honor to be introducing Professor Ken Goldberg from UC Berkeley. I think
many of us you know when we see robots we think about engineering. I think when Ken sees robots he thinks of them as a
form of art. So Ken is not just a roboticist but also an artist. Uh I
think Ken developed you know the first provable algorithm to do part feeding.
Um you know also getting one of the first robots that appeared on the internet. I think in the more recent
years, I think he has done DexNet which maybe many of us know about as being the
de facto work for doing robot grasping when the deep learning revolution was
kickstarting. [snorts] Um, you know, Ken uh went ahead and co-ounded ambidextrous
which I heard is doing it 100 million. I'm giving away my punchline here. Okay.
No, it's okay. [laughter] uh and I think you know Ken also helped
uh get confidence on robot learning where it is today. So you know thank you Ken thank you
for for doing that and to talk about his side you know outside of robotics I think Ken you also
authored some stuff which got nominated for an Emmy award which is you know
super impressive. So with that you know Ken you know welcome to MIT and looking forward to your talk. Oh, thank you very
much, Bulk Kid. I appreciate that. And I'm really glad to be here. I have to say I have so many friends, it turns
out, among the faculty. I see many of them here and I and and just so great read seeing the students and getting to
to to to just hear all the exciting things that are going on. I want to sh I wanted to share this video. Some of you
might have seen it on uh on Twitter X, but this is this was from a couple weeks ago at the uh conference on robot
learning. And so I was just happy to report that humans are still ahead for now. Okay. So, uh, well, I don't know
how long that's going to last. Uh, you've also seen the other news just came out this week. So, we have a, you
know, NEO and, uh, this is the folding quality. Um I'm a little concerned
[laughter] of uh NEO but there's you know a lot of a lot of excitement a lot of interest
and that's what I want to talk about is where we are as a field where this where
the excitement is and I want to and hopefully we'll get some push back and and discussion so I'll leave time for that. I also want to mention that I'm
seeking postocs. If any of you are interested or know of someone please send them my way. I'm actually uh
interested in hiring several postocs right now. And uh I just want to mention I've been doing some research on on
grasping uh just last week uh Friday night in particular I had kids over and
it was fascinating because um you know I would tell the kids just take one candy
and they would just do this kind of ballistic motion which was fascinating to watch that they would just be able to
pop in and take one although I think a few of them palmed a few. Anyway, the
other thing is that kids, you know, we're all actually good at at this, which is different than than than just
picking up one thing, but we can do this multiobject grasping, which is quite fascinating because you can really pick
up, you know, if you pretty much anytime if you said pick up all the objects that are sitting on this table, you could do
it. And that I think is an understudied question. So, let's uh let's get
started. This is where I think I've been waiting for this for all since I was a
kid when I watched the Jetsons. And I want the robot that you could just order. It comes to your house, it cleans
up after itself, it starts doing the chores, and then you know it's ready to play. And uh so now they're we're seeing
this is sort of starting to happen. And you know, all these labs are putting out these beautiful humanoids. And you know,
they look human. They're doing humanlike things. and they're they're they're they're
they're really it's really starting to come. So, it's just like everyone's wondering is is you when is the chat GPT
moment when we're going to have the equivalent of what we had three years ago. It was just about November of 22 when we suddenly opened up our browsers
and there was chat GPT. [snorts] So, and there's a lot at stake here because
well, big names like Elon Musk and um Jensen Wong are basically saying this is this is a massive transformation. This
is a $50 trillion industry and the money that's being poured into these companies as some of
you know is enormous and if you're if you're an entrepreneur Yeah. I know these are all out of date. Exactly.
They've doubled since then. Um you know physical intelligence skilled I mean as
an entrepreneur it's mindboggling that you get these kind of valuations uh just as seed money.
So the numbers are large there's a lot at stake. So let's come back what is the chatbt moment and the hope is that we
can do this in an endto-end fashion. So you give it signals in and you're getting uh actions out and the mantra
that I hear a lot in Silicon Valley is listen large data solved vision large
data solved language therefore large data will solve robotics. And just a
spoiler, I just want to share with you. I believe that will be true. But my question is when? Because
I'm going to share with you some experience, but I'm I'm very concerned about the the time frame and the
expectations that are out there. And part of the problem is that we have you
know the the the analogy is is is kind of problematic because we have you know
vision is a 2D problem if you think about it as um you know matric matrices of numbers. So you have you have 2D in a
language you might think of as a one-dimensional tok string of tokens in [sighs] in robotics you actually have to
produce a series of dimensional data right you have many joints and if you
have one arm it's six if you have two it's 12 then you add the 22 degree of freedom hands or a pair of those hands
you can quickly up to 50 100 degrees of freedom [snorts] and the bigger issue is
we don't have the data there's no data out there nothing's on the internet that tells us what was what there's no
examples [snorts] that are available. So now so the data is the is is a is a big
issue and the data gap I'm going to talk about but just let me give you another argument here which is you know that
that is data all you need and just empirically let's consider uh Whimo so
Whimo is operating in San Francisco I think it's starting in LA it's going to
open up they're they have plans to to to move to other markets And if you had a chance to try this, it's actually really
fun. I say it's like better than anything at Disneyland because you get to go in there, you get in there and you're on city streets and all of a
sudden there's a, you know, a baby carriage and you're like, ah. And it's and it stops and it's really impressive.
Um, these systems are now running and uh in around San Francisco, you really can't go more than a couple blocks
before you see another Whimo in the on the road. So um but let's compare where
Whimo is to its competitor uh Tesla. So Tesla's been also been working on
this problem. They want to have those same taxis. And what's interesting is Tesla has been collecting data for a
while. They have well this is again don't take these numbers literally but just roughly 9 billion miles of of
collected data which is about a factor of 500 to the amount of data that uh that Whimo has. But if you look at
performance, well, this is miles to disengagement. So you want to have as big as number as possible. And Whimo's
way ahead. And so Tesla, this is part of the reason you don't see any Tesla auto
taxis. They're just not safe enough. And now I know there's other reasons. If you
if you if you know about follow these things, Tesla is using just RGB cameras. Whimo is using LAR. So I think that's a
big factor but it's also just that it's it's my point is if data were the only
ingredient then somehow why do we see this huge disparity
and I would tell you that the answer is part is is is is largely that Tesla is
definitely using data. They're training large models in their system but they also use what I call good old-fashioned
engineering. And what do I mean by that? Well, I there's a lot of filters.
There's a lot of procedural elements that are go into this car. And if you just look at the structure, you start to
see it. Particularly, there's modules. There's different sensing modules that are uh that are operating here. And what
I mean is that good old fashioned engineering big the biggest principle might be modularity. One of the things
and you all learn this in your classes. You want to learn components and really understand how they work. And you have
you have very clear encapsulation between modules. They have very clear input and output conditions. And then
there's the idea of composability. You can put them together reliably and you can test them out individually. If
something goes wrong or if something better comes along, you can replace them. So modularity is really really
helpful. Also algorithms we've been learning them for a long time. You you
have they have a lot of benefits. you can actually figure out what's going on and you can fix them. And metrics and
the metrics that have been around in good old fashioned engineering are uh very extraordinary. There's lots of
different sophisticated metrics. So I want to make an argument here today about good oldfashioned engineering and
why it's still valuable. And by the way, this has been noticed in the systems community. And this paper that from some
of my colleagues who who started data bricks was basically making this argument that even systems like chatpt
are not monolithic. They're not just pure endto-end systems. You have you
have a endto-end system um but actually under the hood there's lots of different components. So there may be databases.
There's going to be different kinds of sharding and uh and and elements to scheduling. And now you could talk about
it in terms of agents, right? But there's lots of p pieces that go on to make these systems work and work
reliably. So you can't just it's kind of a myth to think that everything is operating as an end to end. So um and I
also want to say something about scaling laws. This is been very popular. In fact, there was an article that came out
two days ago from uh generalist that's arguing for scaling laws in robotics.
Scaling laws for large models have been around for a while. basically saying that as you add more data you get
improved performance and there's I think this is very true and is no doubt but
the question is we have to think of these in context like how how fast where do we want to get to in terms of where
and do these are these going to asmtote at some point now I'm not an opponent of
data models please don't get me wrong about that I'm a co-author on this gigantic paper uh with along with 150
other people but the um so openx embodiment was a major effort to collect a lot of data and apply it to learning
models and it's it involved lots of labs and lots of uh including my lab at
Berkeley but the idea was to collect data from many different sources many different robots grippers cameras doing
many different tasks and it's a big data set it's got a lot of stuff in it uh one
thing I have uh problem with is the metric which is often just the success
or failure. So it's a binary metric that's per that's applied to the performance on the tasks and so that's
what was reported and you know it's not great. Okay, you're getting like 50 60%
success rates and it's I feel like success is very subjective. is a problematic because oftentimes you're
just looking at it and of course you have a sub biased observer and you know
you're trying to say it's successful but there's a lot more going on here and so what else can we do in terms of um
metrics quality metrics my biggest issue has to do though with the definition of tasks so they claim in the paper that
there's 160,000 different tasks in this data set I I I argued about this but
that was overruled in the paper But um basically if you look at these tasks and
here they did uh we did include this histogram which is just take the textual
description of each task and then um sort of plot them. You see that like the
overwhelming majority like 90% of these tasks are pick object zero and place it
in object one. So of course they're varying object zero and object one. Sometimes you pick up the tiger and put
it in a red bowl. Sometimes you pick up the tiger and put it in a blue bowl. But these are not necessarily different
tasks. And by the way, this task, pick object zero, place in object one. Well,
that's chapter three in Russ's book, right? We know how to do that. We've been doing it for a long time and it's
actually that is a in the classical sense and what we can do it actually quite well. We do it with good
oldfashioned engineering. So modularity, we have a module that probably does some thresholding with a vision, finds the
object, maybe does a little grass planning, then inverse kinematics comes in, gets a gripper over there, close the
gripper, lift, a little more emotion planning, and then release. Right? So that will work very well and pretty
general. So it's this is I want to just make a play plea that you know we should
put just keep this in context because I do think there's a younger generation maybe some of you here who don't know
about this stuff and are thinking you know this is brand new and we not putting it into context that we've we've
actually had this for quite a while. also the metrics just coming back there's all these beautiful metrics that
engineering has developed over the centuries that are very important and
you know things like understanding um uh uh you know the ROC curve and in in in
robotics maybe percent completion is very important you can actually get some information from that it's a continuous
metric or execution time kind of matters because if you're sort of going like this for quite a while that's important
to know about rather than just binary did it succeed or fail etc. So um and I
just to give you more context I we were cleaning out the lab recently and this student found this book which is I think
many of you know this is about a thousand pages of good oldfashioned engineering and he said uh can we uh
let's get rid of this [laughter] and I was like well uh no I mean we there's
there's something I think it's still value valuable to some degree so the way I think about it is look large models
super cool, super fancy, very interesting, but sometimes
good oldfashioned engineering just gets the job done. All right, so [laughter]
all right, so now I'm going to go on a little detour and tell you about um my own experience with with grasping and
um it's going to relate to the to this data story and then we'll talk about scaling. So this starts about 2015. I
was invited to co-e a class on on robot manipulation with Rouja Bichi and uh
Shankar Sastri and some grad students and we used Richard uh sorry um Shankar
and and Shaar's textbook which many of you may have seen or used and it's a beautiful book. It's got basically all
of this matrix exponentials for doing kinematics and also grasp models and it
was uh it was really fun to sort of get back into the thick of all that. But what was also happening at around the
same time was this quiet revolution was burning started to heat up about deep learning and as you know it was fueled
by massive data sets cloud uh uh GPUs and algorithms and we're getting this
kind of results were starting to happen right image labeling was undergoing a transformation and it was deep models
deep learning models were able to to label images faster than ever before. So in particular it was largely due to
image net that was a pretty important foundation that was the source of data that was used to create those kind of
results and it was just a lot of it due to fee Lee her diligence in just collecting vast amounts of data. So we
were working on grasping and I started talking with uh my student at the time
thinking well how can we apply something analogous in the context of manipulation and we started thinking well we need
examples we need lots of data. So we decided to go on a hunt for uh grasping
examples. And so we called it the the goal was DexNet or Dexterity Network in
in homage to imageet. And the idea here was that rather than
images with textual labels, we want to have three-dimensional objects, solid objects with uh with grasps on them. So
we we went on a hunt and uh fortunately Jeff Mer was my PhD student at the time
superb engineer and he inspired a number of undergrads to get on the hunt with him. So we went out and we looked for
threedimensional models all over the internet and there were a lot of things we could find there shaped and various
repositories but also 3D printing was sort of taking off around that time. So people were posting their 3D models
there also a lot of gaming sites etc. So, we just were grabbing images from um uh 3D models from all over. In
particular, we were on the hunt for this kind of thing, what we called um adversarial objects. These are objects
that were not obvious how to print, how to how to grasp them. And so, we were
just pulling all these in. We we we cleaned them up, made them watertight, put them into common uh CAD format, and
then we scaled them, etc. So, we had this large we were just building this collection, and then we started thinking
about the grasps. So typical object in that set might have a thousand facets
and a grasp with a parallel jaw gripper is a pair of facets. So you have a million different ways to grasp the each
of these objects. And so we want a way to analyze the be the quality of these different grasps. So we started thinking
about the fundamental issue of uncertainty. And this is that you're really uncertain
because of of of control, perception, and physics. All three of those are are
are never known precisely and they all conspire together and they add up at the
endector at the grasp location. This is why I think grasping is so challenging and real. But you can characterize this
in a way of with a graphical model. So if you treat all these variables as random variables and then there's
conditional distributions, right? So um the shape of the object may be
uncertain. That's going to affect where the the the the contact normals are. Friction may be uncertain. You get the
point. And so this number at the bottom is the probability that a particular grasp will succeed. Now what we can do
with that model is we can actually sample these distributions. So if this is a
nominal grasp, right? I want to grasp this object here. What I want to do is look at perturbations around that
nominal grasp. So again sampling from the distributions to say this succeeds and this fails. So you get these um
success and failures based on the perturbations and you're sampling a number of them maybe a few hundred or a thousand and you can then add them up to
come up with basically Monte Carlo integration. You come up with a number and that's going to tell you the
probability that these grasp will succeed. So as you see on the left you have a a fairly low a fairly unrose
non-rouss grasp low probability of success that's 22 and here on the right is a a grasp with higher probability of
success. Does that make sense to you intuitively? The one on the left is very brittle to small perturbations. It's
going to fail. The one on the right is is kind of robust to those perturbations. And you're varying things like not only the shape and the position
of the of the gripper and the object, but also the center of mass and the coefficient of friction. Well, once you
have that number, you can then um the next thing is to also factor in sensing.
So, sensing is also inherently uncertain as well. And we wanted to use 3D uh
depth sensors which were which were also popular right around that time and um and we were doing experiments in lab and
we see things like this. So, those sensors are not exactly perfect. there's a lot of noise and it has to do with
specularities or um transparency and all kinds of things cause the uh errors in
the 3D sensors. So this was typical and we were measuring those behaviors and so what we decided to do was to actually
build a model of the sensing um the sensing distributions. And so here we're
going to consider an observation Y that's been corrupted by noise. And so what we want to do is generate examples
and then optimize based on the perception of those of the of the scene. So here's what we're doing is we're
taking we have a known threedimensional object. We're saying what would that look like under one of these noisy
sensors. So this is the depth map that's been uh corrupted with some uh statistical noise. And then these are
some sample grasps on the object. Again these are in 3D. And then we know that number the probability of success. So
that gives us we a a data point and we can generate lots of these in parallel
on the cloud. So we distribute this out over lots of different processors using Google cloud or AWS and then in a few
days we're able to generate say millions of examples of these grasps. Now this is
so the positive examples are grasps again noisy image particular gripper location and a [clears throat]
um a value and then negative are these values where they're low the probability of success is is is small. So these are
the data points and then we just train a network. So we give the data input we know the output as well. We clamp both
ends we we do um gradient descent and we tune a bunch of parameters theta. So we
can basically train this network and we know it works kind of well because we have a held out set and we show it the held out set and it starts uh converging
and so we want to use that in a control loop. So once we have that tuned um set
of parameters what we're going to do is we have a um and we can by the way we can simulate also heaps of objects and
then we have this is like a a bunch of objects in a bin. we can sample a number
of grasp points and then cross entropy we reduce the number of of sample
points. So, we're testing each of those, by the way, with this um uh using the the probability of success based on all
these noisy variables. And that gives us another set. And we keep reducing until we get down to a single grasp that we
believe has the highest probability of success. And then the robot executes that. And here it is performing in in uh
slightly uh faster than real time. But this is uh this was surprising. I mean, I had been working on grasping for a
long time at this point about 30 years. And I had never been able to get anything like this. So it's the the bin
picking problem that um it was had sort of uh challenged roboticists for many
years. And these are all objects that's never seen before, never been trained on. There are also as if you look
there's uh several objects that are deformable. And we trained everything on assuming rigid objects. But it was able
to start picking things up and it's not perfect. You'll see some failures, but it was able to start picking things up
much better than anything I'd seen before. So we uh we got some publicity about this. We were actually on the
front page of the New York Times for about four milliseconds and then we got
some calls from uh companies. So uh companies who wanted to to use this but they wanted a um they wanted suction
grippers and if you industry this is much more common. Now suction is really nice
because it's a single point of contact but we started thinking you have the same kind of scenario. you have
uncertainty in the position of things and you have uncertainty in the physics. So we thought, oh, let's let's try and do the same analogous thing. And we went
to the literature to find uh the the the force model, the wrench model for a
suction cup. And we couldn't find it. And actually in this audience is probably best way to ask, but I've been
I really believe that it's out there that someone has studied this, but I we could not find it in any of the literature. And I still believe it's out
there somewhere, probably solved in like 1842 or something, but um but we
couldn't find a good model of suction cups. So we made our own and this was
something we we the best we could do but basically there's a there's a component of it that measures the quality of the seal based on the local surface geometry
and then a quality of the of the of the strength of the grasp which has to do with the center of mass of the object
and also the um the resistance in this case gra the suction cups are very good
at vertical force but they're not very good at the twist forces. So we could model that and then we could do
something very analogous where we're going to use uh perturbation. So if we wanted to grasp it at that that point
there nominal point yellow there what we're going to consider is a bunch of grasps around there and then evaluate it
with that wrench metric and then rate their probability of success. Then add
these all up and then you come up with something like this where you can score different points on the surface of the object by their suctionability.
So here's a result. This is DexNet and we're using two different modalities in
parallel. And what's nice is we're using one one metric of probability of
success. So we can compare the two grippers and then we're testing which
one of these will be have a higher probability of success and then uh choosing that one. Now, if you watch,
you'll see it fail a few times. And it's not perfect, but it was really
surprising me because I now, you know, these are again objects that we were
just not in the training set. We're throwing all kinds of things in there. We're having a lot of fun. Uh just uh
bringing objects in every day from closets and and and uh and and garages,
etc. and it was able to pick these up and clear out these bins routinely.
So, um we we published this paper. It was in science robotics and then we got
a call from uh this guy. So, that's uh that's Jeff Bezos and he
invited us to he said he he his assistant said we he wants to see this system for himself. Can you bring it
down to his test facility? So, um, it was very nerve-wracking. We had to, uh,
put it on on a truck and take it down there. Completely different, you know, environment. He basically gave us a tent
to set this thing up. So, a lot of pressure and um, but we brought it down
to the kudos to the team of students that got it working and then we had brought like three boxes of objects to
test it out with. So, everything was going great. We're testing it. Bezos was in there. He's like, "This is really interesting." And everything was going
really smoothly. until his assistant Ty Brady pulled off his shoe. Okay, now
let me just tell you, we had never tested it with a shoe. We tried a lot of things, but so when he does this, I was
like, "Oh no." So, I'm going to show you the video because we had it captured
here, but my mouth went dry. Okay. I was just like, "No idea what's going to
happen here." He drops it in. What can we do? We have to let it go. And we're just like watching. I'm holding my
breath. I have no idea. We're all just waiting and
pulls out the shoe. I was so happy. I can't tell you. I called my wife and I
said, "This was the best moment of my life." [laughter] And uh he was pretty happy, too. He
said, "This is a big problem. I've been trying to solve it for a while. You know, you guys you guys have figured something out." Um so uh the students as
we're packing things up they were like let's start a company. So we did we started Ambi Robotics the next week and
this is um this is the team. Fortunately Jeff was about to graduate and another
computer scientist was finishing up and then uh two mechanical engineers uh that were also working in the lab um were
also interested in working together. They're all friends and they all wanted to work. So it was a really nice combination. And so we all co-founded
Ambi and the uh we've been working ever since. So I'm only there periodically
like one day a week, but they're they're in there been designing the systems and working on them. And one of the um the
the the timing was this was in 2018 2019 or 2020 the uh the the pandemic hits.
And so we were looking at different applications and fortunately
uh e-commerce was was considered exempt from this uh from the rules and so we
got an exemption and they let us continue working and we really focused in on package sorting.
So this is for e-commerce systems, right? There's a there was a great increase in e-commerce. So I'll show you our system. It's called Ambi Sort. And
so here is a system. It's a It's a industrial robot arm that can reach in
with suction cups, pick up objects, packages, and then scan them for the zip code and then place them into the
smaller to the smaller bins using a gantry according to destination. So this
is actually a real core problem in almost all distribution centers. And so this was our vision. will sell, you
know, a lot of these individual mechanisms, just the same pretty much the same system, Ambi Sort, to lots of
different customers. And I'm happy to tell you that four years later, we actually have them out there. And the um
they've been running pretty much around the clock. We work with all the major um shipping companies and uh and it's
growing. It's going it's going well. Now, I will say you might you might say, "Well, wait. You just said data wasn't
all you need, but you just told us a data story where the data that you generated was the crucial component
being able to generate this training data. So isn't data all you need? And I will tell you the answer is no because
data played a crucial part in the in that particular piece of this system and
in the grasp quality, but it didn't it didn't solve the whole system. So there
lots of other parts of this system and it's very modular. This uh this uh ambi
sort has elements for different cameras, different filters. There's a lot of safety elements but one big part was the
motion planning and of course I think most of us assume that motion planning is kind of solved
and we know how to do inverse kinematics. But it turns out that doing adverse kinematics fast is still a
challenge. And here it really mattered because you have to be able to move this fairly uh bulky wrist with these suction
cups on it into a crowded bin and pull up an object and get it out fast. So um
we had P controllers by the way also for the gantry and other elements that were in there. Um but we had to develop new
algorithm for grasping for motion planning. And we turned out that we could use deep
learning for a piece of that which is that because we knew something about the general shape of the bin, we could
generate lots of training examples of the robot reaching in from different angles and then train a network to warm
start a motion planner that's based on optimization. So this turned out to be another paper um that uh Jeffnowski is
who's who's now at CMU was the uh lead author and um and it's a it's a it's a
nice way of combining essentially data with good oldfashioned engineering because you're collecting lots of data you're training but that gives you a
warm start that gives you a very fast uh convergence to a solution and so Jeff
and some other students went off and formed Jacobe Robotics. So this is a second company. Jacobe is focused on the
software side and motion planning uh specifically. So it's a platform that
does motion planning for different applications using different robots and sort of has been also focusing on
palletizing. Now another aspect of this is the is the metrics and I would say there were a lot
of metrics that I never thought about in the lab. We were trying to optimize pics per hour. How many objects can you get
out of the bin per hour? And then we got into industry and we found out about double picks. Well, those were
considered good in the lab because you got more things out of the bin, but not very good for industry because if you pull out two objects and they treat them
the same, you're going to somebody's going to get the wrong somebody's not going to get their delivery. So, those
are very bad as we've learned. But, there's all kinds of other factors that come in. And a big one is uptime. Again,
you really don't think about this in a lab, but it's crucial in industry. So, if your system is not running all the
time, if there's a long, if there's short meantime between failure, they're not going to be happy. They're going to send it back.
Okay. So, let's talk about robot scaling. So, again, I want to put this into the context of where we are, where
we're going to get to to get these kind of, you know, the vision here of the humanoid robot that we're going to we've
all been waiting for. When did our when is our chat GPT moment? And um the the hope again is end to end. And I want to
also say I've read the bitter lesson. I'm very appreciative and respectful of Rich Sutton and he you know is a strong
argument right that in so many domains data wins or essentially computation wins. If you let anything that scales
well with computation is going to is going to actually really increase over time with Moore's law. And I get that
and I'm not I want to say I'm not against learning. Okay. Hopefully you don't get that impression. And you know,
I think there are some people in in robotics who are against learning. They really hope that just this this fad goes away. [laughter] You know, we get back
to our good old fashioned engineering. I'm not saying that. I'm actually saying something different, which is that there's a value to putting putting these
together. And I also think there's an equally big danger from the from the
current to the sort of the second faction which are very dogmatic about we don't want any good oldfashioned
engineering. We just want data. [laughter] So um so so again I want to talk about
this thing of data solving vision language and and when will it solve robotics. So um we put together this
little video where it was based on an observation by Michael Black from physical intelligence who basically said
well if you want to compare data sizes let's compare shift everything into hours now to do that so if you want to
train an LLM how much data does it take you think how long would it take a human to read the amount of text that was used
and people read at an average rate of 238 words per minute right so you can do this comparison shift compare all the
things in terms of hours so here's the oxe that the Google project that's physical intelligence. Now we start
looking at some some LLMs right these are early LLMs in comparison you see
quickly that the robotics data is shrinking down in the lower right left corner now smaller sub pixel all right
so quen is is 1.2 two billion hours of data. And so if you convert that into
years, physical intelligence, you know, last year, just about this time, put out pi zero, it's about based on about a
year of of robot data. That's humans telly operation time. Quen is about 100,000 years of human clock time. Okay.
So I know that I'm trying to I'm being a little dramatic here. It's not literal and I know you could quibble but I want
to say there is this robot data gap that is enormous that we really should keep
our eyes open that uh you know even if we have dozens of people working around the clock as is happening we are um we
still have a big gap between the amount the data size and not even to mention
the dimensionality of the data that was needed for robots. So where are we going to get this data? Now one big point that
people are very excited about is simulation and this is um that if we can
simulate we can simulate lots of uh activities we can build up a data set very fast and this is um robots uh it
works very well for robots in um uh flying robots UAVs you can simulate them
very nicely and then you can transfer that into real and so uh this is a a
case where robots have been um flying in these compet competitions and you can beat human performance by training them
in sim. And the other area is in manipulation and so and I'm still
waiting for a really good [sighs] uh reason or answer for this but robots in you can you can train thing robots in
simulation and walking and say rough terrain and that does seem to transfer. So, you know, you can build things like
this and you can just run lots of runs with your favorite humanoid
and after a while it will give you a policy and when you transfer that onto your humanoid it often works and you're
getting results like this which are incredible, right? Every if you're if you're paying attention on Twitter or
something you'll see, you know, amazing results that come out almost every day of of robots doing something else that's
kind of mind-boggling. So it it works really well for flying
and and and locomotion but grasping and manipulation it does not. So empirically
we've done a lot of we as as a community have done a lot of experiments with
manipulation and when you train it in in in say RL or or um in sim those do not
transfer well into practice and it's because of a lot of nuances here. I
think one of the things is that in in um locomotion there's one nice one one
force vector it's very important and that's gravity and you kind of know where that is. It's kind of constant but here you have a lot of forces that are
very difficult to estimate. You have deformations and then here this is kind of phenomenon you see a lot where you
have small interpenetration of the uh bodies that cause jumps in forces and so
you get these discontinuities that are really problematic. So these are very typical when you're trying to simulate.
It's very challenging. Now I I know Russ is going to ask me a question later about that Drake has solved this and I
think is hopefully there is hope and I think there is again many people are working on
ways to address this and I and I I just want to again say I'm not saying it's not going to happen but I just want to
say it's we haven't solved it yet. It's the challenge. Now, YouTube videos is another source of data and you know
there's a lot of of data out there and so Nvidia for example has been building world models and what these are models
that are trying to simulate from a from from vision uh where you have a you give it a few frames and then it completes
the frames and these actually work fairly well. Uh you can use it even where you give it text and it'll
generate frames for you. So here's a text where we gave it to just say grasp this red object and put it in this bin.
Oh, it looks good, right? So, you know, can't we just do this? Well, look more closely and you see that something
really weird is going on, right? It's not actually even touching the other side of the object. And then we ask
Grock to do this and Grock Grock does something even weirder like I don't know
what's going on there, but it adds another finger on the end. Um that uh
yeah, so you know, it's not trustworthy. So I don't think we're there yet on that
front although people are looking at it. How can we generate you know especially from this egocentric uh videos which we
we have a lot of but again there's a lot of occlusion you don't really see what's going on you have to infer and then the
joint components are also very hard to know and forces are difficult. human
teleop is the way that most people are going right now and it's it's actually showing some very nice progress or
promise and examples like this right people are doing it seems like a lot of fun
although some of it looks like a less fun where you people are out in these
factories just uh pulling in lots and lots of examples and you know so let's
come back to oxe which was a basically example in this idea of lots and lots of
demonstration data Now um you know uh physical intelligence is also generating
a lot of this and they're getting some interesting results but I just want to you know just note that I showed this to
my wife and she was like um those folding that's folding is not acceptable
[laughter] and so you know I don't want to pick on them but I just saying that this you know it's not fully solving it so other
companies are working on this but we're trying to get to general purpose robots
we're going to need a lot of data. So there's another way of getting data I just want to mention that I think is not
being not being considered in academia or so much in industry which is using
real production. What I mean by that is um at least in
I'll tell you the example in our our case of ambi where we left off ambi is out there generating um uh uh basically
full sorting packages. Now I mentioned to you the uptime factor right that uptime is very important. So what we did
when we set out when we started installing these systems was uh oh and I I I will share as uh as Pit mentioned
we've sorted 100 million packages over the last four years and um but we've
also put in these uh monitors so that we get data from every one of these systems
uh in real time. So and the reason the reason we did that was was for
maintenance. We want to keep track of all these systems because uptime matters and so as soon as we see something
starting to deviate in performance we can track that and take it uh proactively we can go in and try and fix
it. So we'll call a company and say you know your suction cup might on you know on machine 6 maybe uh isn't isn't
working and so or a camera gets bumped or something like that. So um we were
watching all these systems. We have triggers and warnings set up on all of them and but that is a turns out to be
fairly valuable for just data collection. Now remember we started collecting in 2020 before the chat GPT
and before the sort of excitement around generative models. So we weren't necessarily thinking about using this
data but it was something we ended up storing. And so when we added it up, we
actually have um a good amount of data from from all these uh picking operations. In fact, it's 22 years of
data. So, and I want to say I think this data is valuable because it's
real packages with real robot systems in real customer environments. And so we've
been taking that data and we've only used a small amount of it so far because it's actually very expensive to to build
these to train big models, but we took a a sample of this data and we used it to
train basically a a base system, a pre-trained model. You might think of that as um we call it prime one, but
it's basically a model that's learning to predict threedimensional structure. And then we fine-tune that to pick
objects to train it how to place the suction cups to pick things up. And a key part of this is that we in all of
our training, we did lots of threedimensional objects. So it learned how to read or interpret um um point
clouds, but we didn't have we didn't train it on bags. And bags, as it turns
out, is very very common, increasingly common in um shipping. And bags are particularly subtle to pick up because
you have a lot of wrinkles in bags and these cause problems for your suction cup. So if you treat all these as rigid
objects, you're going to pick a different suction point than you would if you really if you know them as bags.
So this is a case of the sample distribution. We had a we suddenly got this huge amount of data that's right in
distribution for the objects that we actually encounter. So this it turns out that when we run experiments, this is
now running better than the system that we had before. In fact, we also see some scaling effects that as we increase the
number of data, again, we're not able to push this out too far, but we also see a reduction in error, as we increase the
amount of examples. So, we might call this a um a data flywheel where what
we're doing is getting a system out that uses a lot of good oldfashioned engineering and some deep learning to
get it to a point where people will buy it and then once they they're using it, it's generating data that we can use to
improve the system. And actually, I was talking with um Leslie Cabling last night at dinner and she said, you know,
I don't like this flywheel. It's not a flywheel. You don't want it to keep speeding up, right? You sort of you want
it to stabilize. So, she I think Pulkit said, uh, it's more of an avalanche, right? So, I decided to change it now.
So, we'll talk about the data avalanche. Um, but the other aspect is you can use this data to learn adjacent tasks. So,
adjacent task for us is um stacking. If you um picking objects out of a bin
is the duel to that is stacking objects. And so this is actually important for industry too. They want to um stack
objects as densely as possible. And the idea is if you can stack them densely, you can ship them effectively. You can
store them effectively. But this is hard. And actually you probably are familiar with um this problem, right?
It's basically Tetris. And Tetris is a fun game, but it's also been studied.
And in fact there's a paper from Eric Demain that shows that this is NP hard even in two dimensions. So in three
dimensions it's a very it's a very hard problem. How do you efficiently pack uh boxes of differing shapes? And so we uh
when we started out we were getting numbers like this. So, you know, just using a variety of heristics. But what
we did was we ended up using a um and here we actually the symptom real gap is fairly small because we're just treating
these boxes as um solids and then thinking about how you stack them and uh
we used a an alpha zero type of um model where we actually are using re RL and
playing two versions of the system off each other and we got up to 90% of
stacking ability. And this is actually this compares we did a comparison with um with a company with UPS. It showed
that this was actually better than u some of the other systems that they were using. So um so that's the idea. We want
to be able to stack these objects. And then again I want to say that this data data
avalanche now is uh is is the idea that you combine good oldfashioned engineering with um with model free
policies and get a system that works. And then once you have something that works, you put it out there and you then
it's going to generate lots of data and hopefully that data will allow you to improve the product, sell more of it and
then the machines and then you'll get more data etc. So that's the uh that's the avalanche idea. Now I think this
actually is what what's happening with with Whimo coming back to them because they are using good oldfashioned
engineering and and of course deep learning but they're they got a system out and running. They got it to a point
where it was good enough. They got approval. Now it's actually out there collecting more and more data for on
policy uh performance and it's uh it's working for them because then they're
gradually replacing certain of their good old fashioned engineering modules with um learned modules.
This is also I think behind several other companies. One of them is Dina which is um uh based in uh San
Francisco. Jason Ma and some other students put together the system that is folding towels. Okay, it's very
specialized and it's very good at folding towels. In fact, they just trained it to fold one kind of towel.
Okay, the same towel over and over again. But it's amazing because it's very good. These are these are really
nice quality folds. And uh it turns out there's a market for this because
um hospitals, restaurants um uh want a system that will fold
towels and they have the same towel hotels, right? So they actually have customers that pay them to to fold these
towels. What's interesting is that they also did something where that becomes a pre-trained model and then they fine
recently fine-tuned it on shirts and they're able to fold t-shirts with
varying shapes and sizes and actually getting extremely good performance from this. So I think it's an interesting
case of in a sense bottom up approach where rather than trying to be fully general you train something to do
certain task well get it working and then start training to get to keep doing
better and better at that task but also start to perform adjacent tasks. And I think and Russ probably knows
better than me, but I talked to people at at Boston Dynamics yesterday about this and I I will have to say I don't
think I'm giving away any secrets, but this is also I would say a combination of good old fashioned engineering and deep learning in the following sense
that there's the control of this robot is actually MPC. So what the what's
learned is certain key points of where grasp points should happen, but MPC is
taking care of the robot balance and um and and coordination of the joints. So
you get amazing results from that, right? This is this is this this is very impressive. Look at the robustness.
Watch. I love this part where the robot just grabs the bin and slides it back over. It's great. So let me pull this
back into distribution, right? It's going to do this. It's it's very effective. So again, and I I'm fully
anticipating a pointed question from you, Russ, if it's if it's not true, but I think this is a case where, you know,
we we we shouldn't be dogmatic that the the benefits are are enormous by having
um this combination of of of systems and this is also collecting more data. So
there's a data avalanche potential here where it's going to start working as over time maybe you'll get rid of the um
the MPC component. All right. So, we have this gap and um I think it's really
important for especially younger generation uh to to keep in mind that it's going to take some time and that I
think that real production if we're going to start companies uh is a good source. Now, in the last few minutes I
have I'll tell you a few other things which is we've been looking back at this oxe data set and we've been thinking
about how we might be able to actually fine-tune it or improve it. And so one thing we found is that the oaxe is it is
a lot of data but if you want to train a specific policy you want to be able to find the right data to use to train your
policy. Not all data is the same but that turns out to be really hard with the existing oxe you have to find the
right um demonstration category and then within that you have to find the right key frames that you want to train it on.
So both of those things are very challenging. So we developed a system called Robo data management that is
basically a container model that takes the the data sets and puts them into
containers for each demonstration as its own container but it's indexed in terms of these tasks and key frames
and we also do some compression on the video so that we can store it more efficiently. So we've been able to show
that this uh this system actually gives us like fairly big reductions in the overall data size and that gives us much
faster access to pull out trajectories that are needed for learning. Now um so
that's that was work by Eric Chen who's uh just finishing his posttock and it will be on the market and uh the he has
also played a key role along with Shwanu Lei in um
in actually now we're also re-examining this data set and mining it for uh visual language queries. So it turns out
that a big area that uh many people are excited about is that VLMs are actually pretty good at doing spatial um querying
now and but to improve them we can actually go in and look at the oxe data set and extract lots of uh benchmark
queries that can be used to evaluate VLMs but also train VLMs. So they were
able to generate uh just from the the initial pass through oxe 60,000 queries
then then compare different different VLA VLMs on how they perform on those
queries. The other thing is we've been looking into how we can extend the oxe data set
for different modalities different kinds of robots and grippers. So this is the work of Lawrence Chen who just finished
his PhD and he um he's noticing that a lot of the the the examples this is a
different histogram. This is on terms of how how what ARM is used and almost all the data a huge amount is is Franka and
Google robots which are actually no longer that popular. So if you want to um train a new data set or sorry a new
kind of robot or new kind of gripper you're you're out of luck. So what he he's able to do is u by using a series
of tricks of um repainting impainting the different robot. So you can take the data set the demonstration with with a
frana and turn it into a demonstration with a UR5. And so by doing that he's
able to extend basically the um the original data set. This is what we consider the most useful cleaned up
version of the data. And then he's able to expand it again into a data set that's bigger than the original.
And now here's one just two more quick things. This is an observation which is a lot of the manipulation that you see
is things like this and I want to say I think these are really interesting but we should make a distinction between
this is what I would call quasiatic types of uh manipulation and of the
whole manipulation tasks there's an important big subset that are quasiatic and short horizon. This seems to be very
very dominant in the experimentation that we see. Well, what's also interesting is if you look at simulation
and again we're I know there's some experts here but simulation is involves lots of different elements but there's
one piece of it which is the rendering which is taking a system and making it look good. All the other stuff is has to
do with the forces trying to simulate the accurate forces and dynamics that are going on. But the rendering is just
the images and the hypothesis is maybe rendering is is sufficient for the
quasiatic short horizon manipulation. In other words, you don't need all this
extra baggage for manipul for simulation if you just care about quasiatic uh
manipulation. So we have some result there where we developed a system that we call real to render to real. So we're
we're render is we're distinguishing that from full simulation because it's only
rendering the images. But we're able to show that if you just render images of a
of a task, you can train a model on that and then it actually performs decently as long as that task is quasiatic. This
basically depends only on the position of the of the robot rather than on any forces or dynamics.
And then I want to share this which is we've been doing some work on robot assisted surgery and this paper came out
last year. This is a work on using deep learning for um
for surgery. And so we've been working on similar problems to this and uh we were sort of uh interested in in uh this
result. So um one of the things they did was to make it very similar to VA models. They put two wrist cams on each
of the arms. So they had they used six cameras and they were able to achieve um
tying a surgical knot. And the hard part is getting that picking. This is a thing you can do that's twist but grabbing the
uh end loop is very that little piece is very very tricky. But uh my post another
postto Zang Chen uh took this on. And I said, "Let's see how far we can go with just a good oldfashioned engineering
here." And he was able to, we did use data actually to fine-tune a a depth
model. But um he's able to actually generate uh just using one moninocular
camera was able to achieve 12 uh surgical knots pretty reliably. So this
is my my biggest message, which is don't be a purist, okay? Don't don't just think about pure data. Data is not all
you need. that good oldfashioned engineering has a very important role. So if you're interested in that kind of
thing and you're a great to graduate soon, please let me know uh you can find me here goldbergley.edu and I'm happy to
take any questions. Thank you. [applause]
Yes, Daniela.
I want to ask you about data. So, you put this slides up that essentially say,
well, you know, we really need so much more data in order to get the robots to do the right thing, but not all data is
equal. Oh, yeah. We really need a thousand pictures of path in order to understand what a cat is. And so I'm gonna I'm gonna um quote
our friend who at the recent conference said, "Yeah, you know, in robotics we
just learn trajectories. We get a lot of data to learn trajectories and but we used to do that
in the 70s with the teachment. So should we continue to do that?" So my question is, do we have the right data?
Yeah, great question. And you're absolutely right, Daniellea. I think it's a it's a it's a very good point. I
think that there's been a recognition in the in let's say the coral community
conference on robot learning that I watched over the last three years when when oxe first came out there was this
idea all data we just the more data the better just throw all of your data and we'll take anything you've got and and
there was it was interesting because there was people were throwing everything in there there's UAV data in there there's all kinds of stuff that is
like I don't know do we really is this helpful there was no control quality control people cameras pointing all over
the place. When you really look at it, some of it the camera's not even looking at the robot. And it's um so so now
there's a recognition that quality matters, that the quality of the demonstrations actually is very very
important. And in fact, there's a hypothesis that even one bad
demonstration can poison a policy. And I I would love to be able to actually see that pro we could prove that would be
something like the adversarial image results that you could generate an adversarial demonstration that would
actually disrupt a policy's performance. My point was
getting data about trajectories. Is that enough? Well, you mean is do we want more data
about the objects and the environments? not collecting data on the forces and
torsial for well absolutely so I think that for for manipulation for locomotion again it
seems like that seems to be enough right empirically that does seem to work and so I want to give full credit to the
locomotion results that are out there and certain kinds of actions that are quasi static in the the sense I just
described but for everything else and that is not just you're not just talking about high-speed things that are that
that we care about forces. But even something as simple as as um buttoning a shirt or actually my favorite new
example is uh is tying a bow tie, which is something I can't even do. Okay. But
I would love to see a robot learn how to tie a bow tie because there's a lot of nuance subtle forces and torques that
are going on that go that go into that and we're not measuring those and there's a lot of interest. I mean Pokeet
was showing me he's got a lot of exciting new work on grasping and tactile sensors
a lot of excitement about that and obviously TED where is it Ted Adelman as uh the the the godfather of tactile of
optical tactile sensing so a lot of people are also collecting that data right trying to correlate that but it's
very challenging to get to understand what is really going on with all the deformationations that are microscopic
deformations that are happening when you're doing these kind of tasks. So I I agree with you. I think it's not clear
that these teleop tasks are going to get us to being able to solve the full range
of dynamic manipulation tasks. So I agree. Yeah, I think that's right. So that's another layer of difficulty on
top of this challenge. Good. Other questions?
question. All right, Russ, go ahead. [laughter]
I was gonna give him the hardest question possible, but go ahead. I'll go easy. But the the u I mean, the biggest complaint I have with the
picture of the, you know, the Quen's data size versus the the robot. It's just not the way we're doing it. We're
starting with Quen and we're adding data to that. Okay, we get Quen plus all the robot data. All
you have to do is build a bridge from the VLM data. Ah, okay. I feel like the premise is wrong. And
the other question is that is is kind of like you know what what are we actually asking for? We're
not we don't have to write Shakespeare to be successful in manipulation. I think the amount of data is just I think
still open to discussion about how Yeah. Okay. Okay. Good. That was the easy question, the easy version of the question. Yeah. Um, no, first of all, I
I I definitely agree that's a great point that you're actually building on a pre-trained model that is pro VLMs that
are very very good. You're building on top of that, right? So, you get that head start. Absolutely true. But I'm getting at that there's a lot more that
of analogous data to get to the level of performance that you get out of uh, you
know, language models, right, which is astounding generality and ability to to to work that are still mind-blowing to
me. I think that um you're you're absolutely right like there is I think
we're going to make a lot of progress on the quasi static tasks. So being able to stack boxes and do a lot of things that
are actually kind of useful. I'm actually excited about that. But I think that to get into the the range of
generality of real nuance manipulation that is going to be a while. And I think
it's that it's for these reasons that that data we don't have. It's not even clear as Daniellea said that we're that
we're able starting to collect it. Let alone, you know, to build a mo a new new functionalities outside of the
modalities of vision and and language that are that are, you know, these are new dimensions that have to be learned
and where, you know, it's going to take a while to have the analogous thing. I know you he you're you're not sure and I
agree with you. I will be completely happy to be proven wrong and I will eat
my hat and I will but I will say because I could be wrong and that's the other thing I should really really put out that big caveat I I am this is not based
I'm not saying it won't happen right there's no proof in here anything like that and I'm not trying to squash
research in large models I think they're absolutely important and we're doing it right in my lab but I just thinking that
I'm I'm sort of trying to speak to the broader community and the public which I think the public is convinced it's going
to happen next year. So the expectations are super inflated and also let students
know that it's okay to be using these and and be pursuing the good oldfashioned engineering that is the
stuff we're still learning in classes right as far as I know. So don't think that that's all outdated that does
there's actually very important role for these methods and tools and ways of
hybridizing them that I think could be actually useful not only to bootstrap or avalanche data but also to really get
these systems to perform and it might be even for the next 10 or 20 years to get
them to levels that we can actually get them to do something useful. So that's my message. All right. All
right. I thought I was off the hook here. All
right. [laughter] Well, you know, from the uh you know, good old puffs, I know mechanical
engineering, you know, professor's view. Okay. What is missing uh is uh you can say the
dynamics but I know more fundamentally kind of causality. And if you just look at the uh images
like this you know um I don't see any you know real fundamental you know
physical principle and coming from causality and uh you know this also connected to
dynamics and I I I see that the last the 10 millisecond issues up to 10
millisecond a few millcond or or finer stuff it's really critical as you said the manipulations you know this is
really multi- time scale issues something very small scale ones is a less millisecond issues right
I don't think that the current I know trend is really I know having a you know
clear pathway or a methodology dealing with the that kind of fundamental the dynamics
okay so I don't know how you feel about it well that's actually a great topic for discussion I mean I don't have a good answer for that but there is there's a
lot of interest about time scale variations in terms of how these systems are performed how they perform how
they're trained and then how the sampling times because the cameras are sampling at 30 frames a second or 60
frames a second rate. We're not getting that same output rates. We try to match those in various forms, but it certainly
is rarely that you're getting anything under say 5 milliseconds or so in control updates. That's kind of why I
think MPC works nicely with the um Boston Dynamics, right? Because they're running NPC pretty high frequencies to
stabilize the the hand or the body. Um but then you know and and that works in
whole body manipulation but now when you get into say you know tying knots and folding and doing all these kind of
tight packaging and let's say assembly then I think those you're going to need higher frequencies right people say that
tactile is is a thousand hertz or something like that so that's adding a whole another question yeah so I don't
know I don't think anybody's pursuing that at this point although you're looking at tactile I mean do you look at
it as at super high frequencies Please not not for control. Not for control.
Yeah. I think yeah an analogy which I've been thinking about is if you think about humans and if anything goes to the
cortex it's very hard for you to have high frequency control. Same for the spinal cord.
It's a curious question you know how high frequency you need for sensing which I think you still need you know
high high uh frequency to sense but for control it's not clear.
Ah okay. Okay. Interesting. Yeah. Good. But thank you so much, Ken. And we have
you off the hook. Thank you, guys. Thank you. Appreciate it. Thank you. [applause and cheering]


----
### Summary

Here's a summary, with an eye toward your essay on "good old-fashioned engineering" and system calibration.

Core Thesis
Goldberg's central argument: the Silicon Valley mantra — "large data solved vision, large data solved language, therefore large data will solve robotics" — will eventually be true, but not soon. The hype has inflated expectations (people think it's "next year"), and the missing ingredient isn't more data — it's good old-fashioned engineering (GOFE) combined with learning.

What "Good Old-Fashioned Engineering" Means (his definition)
This is the heart of your essay. Goldberg defines GOFE through several principles:

* Modularity — the biggest principle. Clear encapsulation between components, well-defined input/output conditions.
Composability — modules can be combined reliably, tested individually, and swapped out when something breaks or something better arrives.
* Algorithms — long-studied, interpretable, debuggable. "You can figure out what's going on and fix them."
* Metrics — sophisticated, mature measures developed "over the centuries" (ROC curves, percent completion, execution time) vs. crude binary success/failure.
  
His punchline: "Large models are super cool... but sometimes good old-fashioned engineering just gets the job done." And the danger cuts both ways — he warns against both anti-learning purists and dogmatic "data-only" zealots. The right answer is hybridization.

Key Evidence
* Waymo vs. Tesla: Tesla has ~500× more data (9B miles) but Waymo is far ahead on safety. Data alone doesn't explain success — Waymo uses GOFE (modular sensing, filters, procedural elements) plus LiDAR.
* Even ChatGPT isn't monolithic — databases, sharding, scheduling under the hood (Databricks colleagues' argument).
* OpenX-Embodiment critique: claims of "160,000 tasks" are misleading — ~90% are just "pick object 0, place in object 1," which classical engineering already solves well (Chapter 3 of Russ's textbook).
* The data gap is enormous: converting to human-hours, Qwen ≈ 100,000 years of data; robot datasets (pi-zero) ≈ ~1 year. Plus robots have far higher dimensionality (50–100 DoF).